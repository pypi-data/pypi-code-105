from simplebot_cartv import channels


class TestPlugin:
    """Offline tests"""

    def test_cartv(self, mocker, requests_mock) -> None:
        for chan in channels:
            self._requests_mock(requests_mock, chan)
        msg = mocker.get_one_reply("/cartv")
        for chan in channels:
            assert channels[chan] in msg.text

    def test_cartvcv(self, mocker, requests_mock) -> None:
        chan = "cv"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcv").text

    def test_cartvcvi(self, mocker, requests_mock) -> None:
        chan = "cvi"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcvi").text

    def test_cartvcvp(self, mocker, requests_mock) -> None:
        chan = "cvplus"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcvp").text

    def test_cartvtr(self, mocker, requests_mock) -> None:
        chan = "tr"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvtr").text

    def test_cartved(self, mocker, requests_mock) -> None:
        chan = "edu"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartved").text

    def test_cartved2(self, mocker, requests_mock) -> None:
        chan = "edu2"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartved2").text

    def test_cartvmv(self, mocker, requests_mock) -> None:
        chan = "mv"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvmv").text

    def test_cartvcl(self, mocker, requests_mock) -> None:
        chan = "clave"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvcl").text

    def test_cartvca(self, mocker, requests_mock) -> None:
        chan = "caribe"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvca").text

    def test_cartvha(self, mocker, requests_mock) -> None:
        chan = "chabana"
        self._requests_mock(requests_mock, chan)
        assert channels[chan] in mocker.get_one_reply("/cartvha").text

    def _requests_mock(self, requests_mock, chan) -> None:
        data = [
            {
                "title": "Example program",
                "description": "Example description",
                "eventInitialDateTime": "2021-04-25T00:19:00",
                "transmission": "Estreno",
            },
            {
                "title": "Example program 2",
                "description": "Example description 2",
                "eventInitialDateTime": "2021-04-26T00:10:00",
                "transmission": "",
            },
        ]
        requests_mock.get(
            f"https://www.tvcubana.icrt.cu/cartv/{chan}/hoy.php", json=data
        )
