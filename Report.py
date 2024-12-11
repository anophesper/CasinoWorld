class Report:
    def __init__(self, month):
        self.month = month  # Місяць за який надано звіт
        self.withdraw = 0.0  # Сума, яку знято з рахунку
        self.deposit = 0.0  # Сума, яку покладено на рахунок
        self.win = 0.0  # Виграно
        self.loss = 0.0  # Програно
        self.risk_level = 0 # На скільки змінився рівень ризику людини за місяць

    def __str__(self):
        return (f"Місяць: {self.month}\n"
                f"Взяв з рахунку: {self.withdraw}\n"
                f"Поклав на рахунок: {self.deposit}\n"
                f"Виграв: {self.win}\n"
                f"Програв: {self.loss}\n" +
                (f"Рівень ризику змінився на {self.risk_level}" if self.risk_level != 0 else "Рівень ризику не змінився"))

    # ЗАПИСУЄМО ДІЮ В РЕПОРТ ЗА МІСЯЦЬ
    def add_info_report(self, field_name, value):
        # Перевіряємо, чи поле числове (окрім "month")
        if field_name != "month" and isinstance(value, (int, float)):
            # Якщо це числове значення, додаємо до поточного значення
            current_value = getattr(self, field_name)
            setattr(self, field_name, current_value + value)