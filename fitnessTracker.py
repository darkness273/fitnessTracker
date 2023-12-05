class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:} ч.; '
                    'Дистанция: {distance:} км; '
                    'Ср. скорость: {speed:} км/ч; '
                    'Потрачено ккал: {calories:}.')


    def get_message(self) -> str:
        return self.message
    pass


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_times = action
        self.duration_hour = duration
        self.weight_kg = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_times * self.LEN_STEP / self.M_IN_KM
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.get_distance() / self.duration_hour
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__,
                            self.duration_hour, self.get_distance(),
                            self.get_mean_speed(), self.get_spent_calories()))
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время бега."""
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_hour * self.MINUTES_IN_HOUR))
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время ходьбы."""
        CALORIES_MEAN_SPEED_SHIFT_1: float = 0.035
        CALORIES_MEAN_SPEED_MULTIPLIER_1: float = 0.029
        return ((CALORIES_MEAN_SPEED_SHIFT_1 * self.weight_kg
                + (self.get_mean_speed() ** 2 / self.height_cm)
                * CALORIES_MEAN_SPEED_MULTIPLIER_1 * self.weight_kg)
                * (self.duration_hour * self.MINUTES_IN_HOUR))
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_meters = length_pool
        self.count_pool_times = count_pool


    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_SHIFT_2 = 1.1
        return ((self.get_mean_speed() + CALORIES_MEAN_SPEED_SHIFT_2)
                * 2 * self.weight_kg
                * (self.duration_hour * self.MINUTES_IN_HOUR))


    def get_mean_speed(self) -> float:
        return (self.length_pool_meters * self.count_pool_times
                / self.M_IN_KM / (self.duration_hour * self.MINUTES_IN_HOUR))
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_data:
        raise ValueError('Передан неверный идентификатор тренировки.')
    return training_data[workout_type](*data)
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

