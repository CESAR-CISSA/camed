class StreamSchema:
    def get_attribute_names(self) -> list[str]:
        raise NotImplementedError

    def has_attribute(self, name: str) -> bool:
        raise NotImplementedError
