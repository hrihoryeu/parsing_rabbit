import json


class JSONSerialization:
    @staticmethod
    def serialize(val: dict) -> bytes:
        """
        serializing data to sending
        """
        return json.dumps(val).encode()

    @staticmethod
    def deserialize(encoded: bytes):
        """
        deserializing data to receiving
        """
        return json.loads(encoded)
