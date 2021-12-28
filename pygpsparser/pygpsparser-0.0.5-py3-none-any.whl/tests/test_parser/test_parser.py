from pygpsparser.gpsparser import GPSParser


invalid_RMC_1 = 'GNRMC,062357.00,A,2502.3376,N,12133.52528,E,0.132,,231221,,,A*68'
invalid_RMC_2 = '$GNRMC,062357.00,A,2502.3376,N,12133.52528,E,0.132,,231221,,,A'
normal_RMC = '$GNRMC,062357.00,A,2502.3376,N,12133.52528,E,0.132,,231221,,,A*68'
normal_GGA = '$GNGGA,062354.00,2502.3376,N,12133.52528,E,1,05,2.04,254.5,M,16.7,M,,*42'

initial_normal_sentence = \
'$GNRMC,055020.00,V,,,,,,,231221,,,N*60' \
'$GNVTG,,,,,,,,,N*2E' \
'$GNGGA,055020.00,,,,,0,00,99.99,,,,,,*7A' \
'$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E' \
'$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*2E' \
'$GPGSV,3,1,09,03,11,316,,10,19,180,,16,22,220,17,22,23,296,21*7B' \
'$GPGSV,3,2,09,25,23,039,26,26,61,239,34,29,28,081,,31,51,345,*79' \
'$GPGSV,3,3,09,32,70,096,*49' \
'$GLGSV,3,1,09,65,63,320,,66,05,333,,71,13,156,,72,62,164,*6B' \
'$GLGSV,3,2,09,74,20,031,,75,52,332,,76,29,260,,84,03,070,*6F' \
'$GLGSV,3,3,09,85,03,123,*52' \
'$GNGL'

final_normal_sentence = \
'$GNRMC,062354.00,A,2502.3376,N,12133.52528,E,0.134,,231221,,,A*6C' \
'$GNVTG,,T,,M,0.134,N,0.248,K,A*35' \
'$GNGGA,062354.00,2502.3376,N,12133.52528,E,1,05,2.04,254.5,M,16.7,M,,*42' \
'$GNGSA,A,3,26,29,25,16,,,,,,,,,3.12,2.04,2.36*12' \
'$GNGSA,A,3,76,,,,,,,,,,,,3.12,2.04,2.36*1C' \
'$GPGSV,3,1,10,03,17,304,,10,06,174,,16,35,231,34,22,25,281,26*73' \
'$GPGSV,3,2,10,25,10,042,28,26,70,275,18,27,04,193,,29,27,064,24*79' \
'$GPGSV,3,3,10,31,51,010,,32,59,128,07*7E' \
'$GLGSV,3,1,09,65,72,271,,66,19,330,,72,43,172,,74,09,043,*6F'


def test_parse_NMEA():
    parser = GPSParser()
    assert parser.parse_NMEA('') == False
    assert parser.parse_NMEA(invalid_RMC_1) == False
    assert parser.parse_NMEA(invalid_RMC_2) == False
    assert parser.parse_NMEA(normal_RMC) == True
    assert parser.parse_NMEA(normal_GGA) == True
    assert parser.parse_NMEA(initial_normal_sentence) == True
    assert parser.parse_NMEA(final_normal_sentence) == True

def test_parse_date():
    parser = GPSParser()
    assert parser.parse_date('231221') == '2021-12-23'

def test_parse_time():
    parser = GPSParser()
    assert parser.parse_time('062357.00') == '06:23:57'

def test_parse_datetime():
    parser = GPSParser()
    assert parser.parse_datetime(normal_RMC) == '2021-12-23 14:23:57+08:00'

def test_parse_latlon():
    parser = GPSParser()
    assert parser.parse_latlon(normal_RMC, 3, 5) == True
    assert parser.latitude_degree == 25
    assert parser.latitude_minute == 2.3376
    assert parser.longitude_degree == 121
    assert parser.longitude_minute == 33.52528
    assert parser.latlon_radian_RMC == [25.03896, 121.55875466666667]
    assert parser.parse_latlon(normal_GGA, 2, 4) == True
