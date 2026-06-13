from win11toast import toast

class WindowsNotifier:
    @staticmethod
    def notify(title: str, message: str) -> None:
        toast(title, message)