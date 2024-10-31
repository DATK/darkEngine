# 
Engine Docs

Библиотека на данный момент имеет 5 основных классов:

1. MapEditor
2. ImageLoader
3. Vector2
4. GameObject
5. DarkEngineLoop

Процесс создания с описанием классов
Импорт библиотек Vector2, GameObject,DarkEngine(готовый экземпляр класса, а не сам класс),ImageObject,IamgeLoader; В основе лежит PyGame

1. Класс GameObject используется для создания игрового объекта
GameObject представляет из себя пример объекта который можно агрузить в движок
При создании своего объека,вы создаете класс объетка, который наследуется от GameObject
Пример

class Player(GameObject):

    def Awake(self):
        #your code
        super.Awake()

    def Start(self):
        #your code
        super.Start()

    def Update(self):
        #yoyr code
        super.Update()

Player()

Подробнее о методах и свойствах GameObject

Position: Vector2 -> позиция объекта

Sprite: Surface -> Спрайт

Drawing: bool -> Рисуется ли объект на сцене

Width,Height: float -> высота и ширина спрайта

ChekColider: bool -> проверять ли у даннго объекта столкновения

CanGarbage: bool -> Может ли этот объект обрабатываться сборщиком мусора

Enabled: bool -> Активен\Неактивен объект

Awake() -> метод инициализации объекта для MapEditor

Start() -> метод инициализации объекта в DarkEngine

Set_Sprite(pg.surface) -> загружает тектсуру из фото

Load_Sprite() -> Surface -> аналагично методы выше, но создает пустой спрайт, который можно заполнить self.Sprite.fill((255,255,255)) rgb color

если не вызвывать методы создания спрайта, то объект не будет рисоваться

AddSelfColider() -> Включает обработку столкновений объекта

OnColliderCurrent(object) -> Вызывется при пересечении с другим объектом -> object

OnGarbage() -> Вызывается при перед попадаем объекта в мусор

Update() -> Вызывается каждый frame

При инициализации объекта, он автоматически загружается в движок

2. ImageObject

Пример

class PhoneMenu(ImageObject):

    def Awake(self):
        #your code
        super.Awake()

    def Start(self):
        #your code
        super.Start()

    def Update(self):
        #yoyr code
        super.Update()



Position: Vector2 -> позиция объекта

Sprite: Surface -> Спрайт

Drawing: bool -> Рисуется ли объект на сцене

Width,Height: float -> высота и ширина спрайта

Enabled: bool -> Активен\Неактивен объект


Awake() -> метод инициализации объекта для MapEditor

Start() -> метод инициализации объекта в DarkEngine

Update() -> для динамичных изображений

Load_Image(pg.surface) -> загрузка изображения

ColorImage(color: rgb) -> Затычка, делает квадрат n цвета

3. Vector2() -> Стандартный вектор с 2 параметрам x,y и стандартными операциями с векторами

4. MapEditor()

Позже



5.DarkEngine

В движок автоматически добавляются инициализированные объекты

Set_resolution((1280,720),fullscren: bool) -> Сменить разрешение

run() -> Запустить движок