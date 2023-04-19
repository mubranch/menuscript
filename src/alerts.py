from rumps import alert, notification


class Alert:
    def __init__(
        self,
        title: str,
        message: str,
        subtitle="Menuscript",
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.message = message

    def alert(self) -> None:
        alert(title=self.title, subtitle=self.subtitle, message=self.message)

    def notification(self) -> None:
        notification(title=self.title, subtitle=self.subtitle, message=self.message)
