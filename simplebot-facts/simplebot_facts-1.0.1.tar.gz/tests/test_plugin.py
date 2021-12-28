class TestPlugin:
    def test_fact(self, mocker, lp):
        msg = mocker.get_one_reply("/fact")
        assert "#Fact" in msg.text

    def test_factOfTheDay(self, mocker, lp):
        msg = mocker.get_one_reply("/factOfTheDay")
        assert "#Fact" in msg.text

    def test_category(self, mocker, lp):
        msg = mocker.get_one_reply("/factLifeHacks")
        assert "#LifeHacks" in msg.text
