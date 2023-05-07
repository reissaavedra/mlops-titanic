import zipfile


class Preprocessor:
    @staticmethod
    def decompress_file(path_input: str, path_output: str):
        with zipfile.ZipFile(path_input, 'r') as zip_ref:
            zip_ref.extractall(path_output)
        return path_output
