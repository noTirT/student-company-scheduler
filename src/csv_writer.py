class CSVWriter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def to_csv(file_name: str, content: list[dict]):
        if len(content) == 0:
            return
        to_write = ";".join(content[0].keys())
        to_write += "\n"
        for point in content:
            to_write += ";".join(map(lambda x: str(x), point.values()))
            to_write += "\n"
        with open(file_name, "w") as csv_file:
            csv_file.write(to_write)
