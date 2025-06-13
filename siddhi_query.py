class SiddhiQuery:
    def __init__(self, name: str, query_string: str):
        self.name = name
        self.query_string = query_string.strip()
        self._validate_query()

    def _validate_query(self):
        required_keywords = ["@info", "from", "select"]
        missing = [kw for kw in required_keywords if kw not in self.query_string.lower()]
        if missing:
            raise ValueError(f"The query is malformed. Missing keywords: {missing}")

        if f"@info(name = '{self.name}')" not in self.query_string:
            raise ValueError(f"The query must contain the correct annotation: @info(name = '{self.name}')")

    def __str__(self):
        return self.query_string
