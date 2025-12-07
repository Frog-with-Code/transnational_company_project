from company.common.location import Location, Region

class TestLocation:
    def test_creation(self):
        loc = Location(
            region=Region.EUROPE,
            country="Belarus",
            city="Minsk",
            street="Lenina",
            building="1"
        )
        assert loc.region == Region.EUROPE
        assert loc.country == "Belarus"
        assert loc.city == "Minsk"

    def test_equality(self):
        loc1 = Location(Region.EUROPE, "Belarus", "Minsk", "St", "1")
        loc2 = Location(Region.EUROPE, "Belarus", "Minsk", "St", "1")
        loc3 = Location(Region.EUROPE, "Poland", "Warsaw", "St", "1")
        
        assert loc1 == loc2
        assert loc1 != loc3

    def test_str_representation(self):
        loc = Location(Region.NORTH_AMERICA, "USA", "NY", "5th Ave", "10")
        s = str(loc)
        assert "USA" in s
        assert "NY" in s
        assert "5th Ave" in s
