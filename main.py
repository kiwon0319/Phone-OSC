import asyncio
import datetime
import json
from time import localtime, time
from pythonosc import udp_client, osc_server, dispatcher
import win32api
import enum
import math
import ephem
from win32con \
    import VK_MEDIA_NEXT_TRACK, VK_MEDIA_PLAY_PAUSE, VK_MEDIA_PREV_TRACK, KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus


# server port: 9001 (to this)
# client port: 9000 (to vrc)


class Theme(enum.Enum):
    light = 0
    dark = 1
    system = 2


class Config:
    def __init__(self):
        # <NETWORK>
        self.ip: str = "127.0.0.1"
        self.sender_port: int = 9000
        self.receiver_port: int = 9001
        # </NETWORK>

        # <VRC PATH>
        self.path_avatar_parameter = "/avatar/parameters/"
        self.path_chatbox = ""
        # </VRC PATH>

        # <PARAMETER>
        self.address_year = "year"
        self.address_month = "month"
        self.address_mday = "mday"
        self.address_wday = "wday"

        self.address_hour = "hour"
        self.address_minute = "minute"
        self.address_second = "second"

        self.address_ftime = "float_time"
        self.address_fmday = "float_mday"

        self.address_next = "btn_next"
        self.address_prev = "btn_prev"
        self.address_pause = "btn_pause"

        self.address_isPlaying = "isPlaying"
        # </PARAMETER>

        # <APP SETTING>
        self.theme = Theme.system.value
        # </APP SETTING>

        self.load_config()

    def load_config(self, _file: str = "./config.json") -> int:
        """
        :param _file: [optional] (String) file path that have setting value (json format)
        :return: (Int) errno more information see this page https://docs.python.org/3/library/errno.html
        """
        try:
            with open(_file, 'r', encoding='utf-8') as f:
                raw = json.load(f)

                self.ip = raw["ip"]
                self.sender_port = raw["sport"]
                self.receiver_port = raw["rport"]

                self.path_avatar_parameter = raw["VRCPath"]["avatar_parm"]
                self.path_chatbox = raw["VRCPath"]["chatbox"]

                self.address_year = raw["parm"]["year"]
                self.address_month = raw["parm"]["month"]
                self.address_mday = raw["parm"]["mday"]
                self.address_wday = raw["parm"]["wday"]

                self.address_hour = raw["parm"]["hr"]
                self.address_minute = raw["parm"]["min"]
                self.address_second = raw["parm"]["sec"]

                self.address_ftime = raw["parm"]["ftime"]
                self.address_fmday = raw["parm"]["fmday"]

                self.address_prev = raw["parm"]["prev"]
                self.address_pause = raw["parm"]["play/pause"]
                self.address_next = raw["parm"]["next"]

                self.address_isPlaying = raw["parm"]["isPlaying"]

                self.theme = raw["theme"]

            return 0

        except IOError as e:
            return e.errno
        except Exception as e:
            return -1

    def save_config(self, _path: str = "./config.json") -> int:
        """
        :param _path: [optional] (String) file path that config file saved
        :return: (Int) errno more information see this page https://docs.python.org/3/library/errno.html
        """
        try:
            with open(_path, "w", encoding='utf-8') as f:
                f.write(self.tojson())
                return 0
        except IOError as e:
            print(e)
            return e.errno
        except Exception as e:
            print(e)
            return -1

    def tojson(self) -> str:
        """
        :return: (String) convert class variable to json format string
        """
        dic = {
            "ip": self.ip,
            "sport": self.sender_port,
            "rport": self.receiver_port,

            "VRCPath": {
                "avatar_parm": self.path_avatar_parameter,
                "chatbox": self.path_chatbox
            },

            "parm": {
                "year": self.address_year,
                "month": self.address_month,
                "mday": self.address_mday,
                "wday": self.address_wday,

                "hr": self.address_hour,
                "min": self.address_minute,
                "sec": self.address_second,

                "ftime": self.address_ftime,
                "fmday": self.address_fmday,

                "prev": self.address_prev,
                "play/pause": self.address_pause,
                "next": self.address_next,

                "isPlaying": self.address_isPlaying
            },
            "theme": self.theme
        }

        return json.dumps(dic, sort_keys=False, indent=4)


class Receiver:
    @staticmethod
    def receiver_handler(address, *args):
        print("\033[32m" + "{}: {}".format(address, args) + "\033[0m")

        path = C.path_avatar_parameter

        if address == path + C.address_prev:
            Media.prev(args[0])
        elif address == path + C.address_next:
            Media.next(args[0])
        elif address == path + C.address_pause:
            Media.pause(args[0])

    @staticmethod
    def build_dispatcher(lst: list, path: str = "/avatar/parameters/"):
        d = dispatcher.Dispatcher()
        for prm in lst:
            d.map(path + prm, Receiver.receiver_handler)

        return d

    def __init__(self, _dispatcher: dispatcher.Dispatcher, _ip: str = "127.0.0.1", _port: int = 9001):
        self.ip = _ip
        self.port = _port
        self.dispatcher = _dispatcher

        self.server = osc_server.AsyncIOOSCUDPServer(
            (self.ip, self.port),
            self.dispatcher,
            asyncio.get_event_loop()
        )

        self.transport = None
        self.protocol = None

        print("server has been created ({}:{})".format(self.ip, self.port))

    async def start(self):
        self.transport, self.protocol = await self.server.create_serve_endpoint()

        return self.transport


class Sender:

    def __init__(self, _ip: str = "127.0.0.1", _port: int = 9000):
        self.client = None
        self.configure(_ip, _port)

    def configure(self, _ip: str = "127.0.0.1", _port: int = 9000):
        self.client = udp_client.SimpleUDPClient(_ip, _port)
        print("client has been created ({}:{})".format(_ip, _port))

    async def send(self, ctx, parm: str, path: str = "/avatar/parameters/"):
        full_path = path + parm
        self.client.send_message(full_path, ctx)


class SendTime:
    @staticmethod
    def time2float(_struct):
        hour = _struct.tm_hour
        minute = _struct.tm_min
        second = _struct.tm_sec
        m_day = _struct.tm_mday

        if hour >= 12:
            hour = hour - 12

        total_sec = hour * 3600 + minute * 60 + second

        return total_sec / (12 * 3600), m_day / 31

    @staticmethod
    async def time(sender: Sender):
        stamp = time()
        local_time_struct = localtime(stamp)

        await sender.send(local_time_struct.tm_hour, C.address_hour)
        await sender.send(local_time_struct.tm_min, C.address_minute)
        await sender.send(local_time_struct.tm_sec, C.address_second)

        await asyncio.sleep(1)

        print("time send complete!: {}".format(local_time_struct))

    @staticmethod
    async def date(sender: Sender):
        stamp = time()
        local_time_struct = localtime(stamp)

        await sender.send(local_time_struct.tm_year, C.address_year)
        await sender.send(local_time_struct.tm_mon, C.address_month)
        await sender.send(local_time_struct.tm_mday, C.address_mday)
        await sender.send(local_time_struct.tm_wday, C.address_wday)

        await asyncio.sleep(100)

        print("date send complete!: {}".format(local_time_struct))

    @staticmethod
    async def all(sender: Sender):
        stamp = time()
        local_time_struct = localtime(stamp)

        await sender.send(local_time_struct.tm_hour, C.address_hour)
        await sender.send(local_time_struct.tm_min, C.address_minute)
        await sender.send(local_time_struct.tm_sec, C.address_second)

        await sender.send(local_time_struct.tm_year, C.address_year)
        await sender.send(local_time_struct.tm_mon, C.address_month)
        await sender.send(local_time_struct.tm_mday, C.address_mday)
        await sender.send(local_time_struct.tm_wday, C.address_wday)

        print("send complete!: {}".format(local_time_struct))

    @staticmethod
    async def time_float(sender: Sender):
        stamp = time()
        local_time_struct = localtime(stamp)

        float_time, float_mday = SendTime.time2float(local_time_struct)

        await sender.send(float_time, C.address_ftime)
        await sender.send(float_mday, C.address_fmday)

        print("send complete!: {}".format(float_time))


class Media:
    @staticmethod
    def pause(ispressed: bool):
        if ispressed:
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
        else:
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 1, KEYEVENTF_KEYUP, 0)

    @staticmethod
    def next(ispressed: bool):
        if ispressed:
            win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
        else:
            win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_KEYUP, 0)

    @staticmethod
    def prev(ispressed: bool):
        if ispressed:
            win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)
        else:
            win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_KEYUP, 0)

    @staticmethod
    async def get_media_info():
        sessions = await MediaManager.request_async()

        cur_session = sessions.get_current_session()
        if cur_session:
            info = await cur_session.try_get_media_properties_async()
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            info_dict['genres'] = list(info_dict['genres'])

            for key in info_dict.copy().keys():
                if key not in ['artist', 'title']:
                    info_dict.pop(key)

            if cur_session.get_playback_info().playback_status == PlaybackStatus.PLAYING:
                info_dict["isPlaying"] = True
            elif cur_session.get_playback_info().playback_status == PlaybackStatus.PAUSED:
                info_dict["isPlaying"] = False

            return info_dict

    @staticmethod
    async def send_media(_sender: Sender):
        info = await Media.get_media_info()

        if info:
            print(info)
            is_playing = info["isPlaying"]
        else:
            is_playing = False

        await _sender.send(is_playing, C.address_isPlaying)
        print("send complete!: \"isPlaying\" {}".format(is_playing))


class SendMoonPhase:
    _moon_position: float = None
    _moon_type: int = None
    _last_update: str = ""

    def __init__(self):
        self.set_data()

    def set_data(self):
        _stamp = time()
        _localtime_struct = localtime(_stamp)

        date = ephem.Date(datetime.date(_localtime_struct.tm_year, _localtime_struct.tm_mon, _localtime_struct.tm_mday))

        nnm = ephem.next_new_moon(date)
        pnm = ephem.previous_new_moon(date)

        self._moon_position = ((date - pnm) / (nnm - pnm)) * 28

        # moon type
        if self._moon_position < 0:  # error (out of range)
            self._moon_type = -1
        elif self._moon_position < 0.5:  # New moon
            self._moon_type = 0
        elif self._moon_position < 6.5:
            self._moon_type = 1
        elif self._moon_position < 7.5:
            self._moon_type = 2
        elif self._moon_position < 13.5:
            self._moon_type = 3
        elif self._moon_position < 14.5:  # Full moon
            self._moon_type = 4
        elif self._moon_position < 20.5:
            self._moon_type = 5
        elif self._moon_position < 21.5:
            self._moon_type = 6
        elif self._moon_position < 27.5:
            self._moon_type = 7
        elif self._moon_position <= 28:
            self._moon_type = 0  # New Moon
        else:
            self._moon_type = -2  # error (Out of range)

        self._last_update = "{}.{}.{}".format(_localtime_struct.tm_year,
                                              _localtime_struct.tm_mon,
                                              _localtime_struct.tm_mday)

        print("data updated! ({})".format(self._last_update))

    def _update_check(self):
        cur = localtime(time())
        cur = "{}.{}.{}".format(cur.tm_year, cur.tm_mon, cur.tm_mday)

        if cur != self._last_update:
            print("data updated")
            self.set_data()

    def get_moon_position(self):
        self._update_check()
        return self._moon_position

    def get_moon_type(self):
        self._update_check()
        return self._moon_type

    async def send_moon_position(self, _sender: Sender):
        self._update_check()
        await _sender.send(self._moon_position, "moon_position")
        print("send complete!: \"moon_position\" - {}".format(self._moon_position))

    async def send_moon_type(self, _sender: Sender):
        self._update_check()
        await _sender.send(self._moon_type, "moon_type")
        print("send complete!: \"moon_type\" - {}".format(self._moon_type))


async def sender_loop(sender: Sender):
    moon_phase = SendMoonPhase()
    while (True):
        try:
            asyncio.create_task(SendTime.all(sender))
            asyncio.create_task(Media.send_media(sender))
            asyncio.create_task(SendTime.time_float(sender))
            asyncio.create_task(moon_phase.send_moon_type(sender))
            asyncio.create_task(moon_phase.send_moon_position(sender))
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected")
            break


async def start(_ip="127.0.0.1", _receiver_port=9001, _sender_port=9000):
    sender = Sender(_ip, _sender_port)

    parm_lst = ["btn_prev", "btn_next", "btn_pause"]
    d = Receiver.build_dispatcher(parm_lst)
    receiver = Receiver(d, _ip, _receiver_port)

    transport = await receiver.start()
    await sender_loop(sender)
    transport.close()


if __name__ == '__main__':
    global C

    C = Config()
    C.save_config()
    asyncio.run(start(C.ip, C.receiver_port, C.sender_port))

# Press the green button in the gutter to run the script.
