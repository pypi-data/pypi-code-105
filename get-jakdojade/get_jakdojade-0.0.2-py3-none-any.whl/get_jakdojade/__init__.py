import datetime
import enum
import logging
import typing
import urllib.parse

logger = logging.getLogger(__name__)


class Type(enum.IntEnum):
    OPTIMAL = 0
    COMFORTABLE = 1
    FAST = 2


class Vehicles(enum.Enum):
    BUS = 'bus'
    TRAM = 'tram'
    SUBWAY = 'subway'
    TRAIN = 'train'
    MICROBUS = 'microbus'
    TROLLEYBUS = 'trolleybus'
    WATER_TRAM = 'waterTram'


class LocationType(enum.Enum):
    """Not sure about location types, so I do not require parameter to be LocationType"""
    LOCATION_TYPE_STOP = 'LOCATION_TYPE_STOP'
    LOCATION_TYPE_COORDINATE = 'LOCATION_TYPE_COORDINATE'


class InsufficientParameters(Exception):
    pass


def generate(
        *,
        city: str,
        prepare_search: bool = False,
        strict: bool = False,
        from_coordinate_latitude: typing.Optional[str] = None,
        from_coordinate_longitude: typing.Optional[str] = None,
        from_name: typing.Optional[str] = None,
        from_type: typing.Optional[str] = None,
        to_type: typing.Optional[str] = None,
        from_stop_name: typing.Optional[str] = None,
        from_stop_code: typing.Optional[str] = None,
        to_coordinate_latitude: typing.Optional[str] = None,
        to_coordinate_longitude: typing.Optional[str] = None,
        to_name: typing.Optional[str] = None,
        to_stop_name: typing.Optional[str] = None,
        to_stop_code: typing.Optional[str] = None,
        date: typing.Optional[datetime.date] = None,
        time: typing.Optional[datetime.time] = None,
        date_time: typing.Optional[datetime.datetime] = None,
        trip_type: typing.Optional[Type] = None,
        is_arrival: typing.Optional[bool] = None,
        avoid_changes: typing.Optional[bool] = None,
        avoid_buses: typing.Optional[bool] = None,
        prohibited_vehicles: typing.Optional[typing.List[Vehicles]] = None,
        prohibited_operators: typing.Optional[typing.List[str]] = None,
        avoid_expresses: typing.Optional[bool] = None,
        avoid_zonal: typing.Optional[bool] = None,
        only_low_floor: typing.Optional[bool] = None,
        roads_on: typing.Optional[bool] = None,
        avoid_lines: typing.Optional[typing.List[str]] = None,
        prefer_lines: typing.Optional[typing.List[str]] = None,
        number: typing.Optional[int] = None,
        minimal_charge_time: typing.Optional[int] = None,
) -> str:
    query_dict: typing.Dict[str, typing.Any] = {}

    if from_coordinate_latitude and from_coordinate_longitude:
        query_dict['fc'] = f'{from_coordinate_latitude}:{from_coordinate_longitude}'
    elif from_coordinate_latitude or from_coordinate_longitude:
        error_message = (
            "Both from_coordinate_latitude and from_coordinate_longitude required to set destination coordinates!"
        )
        if strict:
            raise InsufficientParameters(error_message)
        logger.warning(f"{error_message} Omitting...")
    if from_name:
        query_dict['fn'] = from_name
    if from_stop_name:
        query_dict['fsn'] = from_stop_name
    if from_stop_code:
        query_dict['fsc'] = from_stop_code
    if from_type:
        query_dict['ft'] = from_type
    if to_type:
        query_dict['tt'] = to_type
    if to_coordinate_latitude and to_coordinate_longitude:
        query_dict['tc'] = f'{to_coordinate_latitude}:{to_coordinate_longitude}'
    elif to_coordinate_latitude or to_coordinate_longitude:
        error_message = (
            "Both to_coordinate_latitude and to_coordinate_longitude required to set destination coordinates."
        )
        if strict:
            raise InsufficientParameters(error_message)
        logger.warning(f"{error_message} Omitting...")
    if to_name:
        query_dict['tn'] = to_name
    if to_stop_name:
        query_dict['tsn'] = to_stop_name
    if to_stop_code:
        query_dict['tsc'] = to_stop_code

    if date_time:
        date = date_time.date()
        time = date_time.time()
    if date:
        query_dict['d'] = date.strftime('%d.%m.%y')
    if time:
        query_dict['h'] = time.strftime('%H:%M')
    _apply_boolean(query_dict, 'ia', is_arrival)
    if trip_type is not None:
        query_dict['t'] = trip_type.value
    _apply_boolean(query_dict, 'aac', avoid_changes)
    _apply_boolean(query_dict, 'aab', avoid_buses)
    if prohibited_vehicles:
        query_dict['apv'] = ','.join([v.value for v in prohibited_vehicles])
    if prohibited_operators:
        query_dict['apo'] = ','.join(prohibited_operators)
    _apply_boolean(query_dict, 'aax', avoid_expresses)
    _apply_boolean(query_dict, 'aaz', avoid_zonal)
    _apply_boolean(query_dict, 'aol', only_low_floor)
    if roads_on is not None:
        if roads_on:
            query_dict['aro'] = 1
        else:
            query_dict['aro'] = 0
    if avoid_lines:
        query_dict['aal'] = ','.join(avoid_lines)
    if prefer_lines:
        query_dict['apl'] = ','.join(prefer_lines)
    if number:
        query_dict['n'] = number
    if minimal_charge_time:
        query_dict['act'] = minimal_charge_time

    query = urllib.parse.urlencode(query_dict)
    if prepare_search:
        search_now = ''
    else:
        if not all([
            from_coordinate_latitude,
            from_coordinate_longitude,
            to_coordinate_longitude,
            to_coordinate_latitude,
            date,
            time,
        ]):

            error_message = (
                "'Search now' does not work without all coordinates: "
                "from_coordinate_latitude, "
                "from_coordinate_longitude, "
                "to_coordinate_longitude, "
                "to_coordinate_latitude, "
                "date and time or date_time."
            )
            if strict:
                raise InsufficientParameters(error_message)
            logger.warning(error_message)
        search_now = 'z----do--'
    return f'https://jakdojade.pl/{city}/trasa/{search_now}?{query}'


def _apply_boolean(query_dict: dict, parameter_name: str, value: typing.Optional[bool] = None):
    if value is not None:
        if value:
            query_dict[parameter_name] = 'true'
        else:
            query_dict[parameter_name] = 'false'
