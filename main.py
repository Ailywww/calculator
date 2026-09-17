import math
import cmath
import flet as ft


def main(page: ft.Page):
    page.title = "Математический калькулятор"
    page.bgcolor = ft.Colors.WHITE
    page.padding = 12
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    stroka = {"value": ""}

    # -----------------------------
    # Приветствие
    # -----------------------------

    welcome_ru = ft.Text(
        value="Добро пожаловать",
        size=24,
        color="#263238",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    welcome_en = ft.Text(
        value="Welcome",
        size=18,
        color="#555555",
        text_align=ft.TextAlign.CENTER,
    )

    # -----------------------------
    # Экран калькулятора
    # -----------------------------

    rezultat = ft.Text(
        value="0",
        size=32,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.RIGHT,
        weight=ft.FontWeight.BOLD,
    )

    ekran = ft.Container(
        content=ft.Row(
            [rezultat],
            alignment=ft.MainAxisAlignment.END,
        ),
        bgcolor="#171717",
        padding=15,
        height=90,
        border_radius=12,
    )

    # -----------------------------
    # Математические функции
    # -----------------------------

    def sin_deg(x):
        return math.sin(math.radians(x))

    def cos_deg(x):
        return math.cos(math.radians(x))

    def tan_deg(x):
        if abs(math.cos(math.radians(x))) < 1e-12:
            raise ValueError("Тангенс не существует")

        return math.tan(math.radians(x))

    def sqrt_func(x):
        if x < 0:
            return cmath.sqrt(complex(x, 0))

        return math.sqrt(x)

    # -----------------------------
    # Показать результат
    # -----------------------------

    def pokazat(tekst=None):
        if tekst is None:
            tekst = stroka["value"]

        if not tekst:
            rezultat.value = "0"
        else:
            rezultat.value = tekst.replace("sqrt(", "√(")

        page.update()

    # -----------------------------
    # Вычисление
    # -----------------------------

    def vychislit(primer):
        primer = primer.replace("×", "*")
        primer = primer.replace("÷", "/")

        proverka = (
            primer
            .replace("sin", "")
            .replace("cos", "")
            .replace("tan", "")
            .replace("sqrt", "")
        )

        razresheno = set("0123456789.+-*/() ")

        if not set(proverka).issubset(razresheno):
            raise ValueError("Недопустимые символы")

        bezopasno = {
            "__builtins__": {},
            "sin": sin_deg,
            "cos": cos_deg,
            "tan": tan_deg,
            "sqrt": sqrt_func,
        }

        return eval(primer, bezopasno, {})

    # -----------------------------
    # Красивый вывод числа
    # -----------------------------

    def krasivoe_chislo(value):

        if isinstance(value, complex):
            real = 0 if abs(value.real) < 1e-12 else value.real
            imag = 0 if abs(value.imag) < 1e-12 else value.imag

            if imag == 0:
                return f"{real:g}"

            if real == 0:

                if abs(imag - 1) < 1e-12:
                    return "i"

                if abs(imag + 1) < 1e-12:
                    return "-i"

                return f"{imag:g}i"

            sign = "+" if imag >= 0 else "-"

            return f"{real:g} {sign} {abs(imag):g}i"

        if isinstance(value, float):

            if abs(value) < 1e-12:
                value = 0.0

            if value.is_integer():
                return str(int(value))

            return f"{value:g}"

        return str(value)

    # -----------------------------
    # Нажатие "="
    # -----------------------------

    def poschitat():

        try:
            primer = stroka["value"]

            if not primer:
                return

            answer = vychislit(primer)

            vyvod = krasivoe_chislo(answer)

            stroka["value"] = vyvod

            pokazat(vyvod)

        except ZeroDivisionError:

            stroka["value"] = ""

            pokazat("Деление на 0")

        except ValueError as error:

            stroka["value"] = ""

            if str(error) == "Тангенс не существует":
                pokazat("tan не существует")
            else:
                pokazat("Ошибка")

        except Exception:

            stroka["value"] = ""

            pokazat("Ошибка")

    # -----------------------------
    # Добавление sin / cos / tan
    # -----------------------------

    def dobavit_funkciyu(name):

        if stroka["value"] == "0":
            stroka["value"] = ""

        stroka["value"] += f"{name}("

        pokazat()

    # -----------------------------
    # Обработка кнопок
    # -----------------------------

    def knopka_nazhata(e):

        simvol = e.control.data

        # AC
        if simvol == "AC":

            stroka["value"] = ""

            pokazat()

            return

        # C
        if simvol == "C":

            stroka["value"] = stroka["value"][:-1]

            pokazat()

            return

        # sin / cos / tan
        if simvol in ("sin", "cos", "tan"):

            dobavit_funkciyu(simvol)

            return

        # Корень
        if simvol == "√":

            if stroka["value"] == "0":
                stroka["value"] = ""

            stroka["value"] += "sqrt("

            pokazat()

            return

        # Равно
        if simvol == "=":

            poschitat()

            return

        # Остальные кнопки
        if stroka["value"] == "0":
            stroka["value"] = ""

        stroka["value"] += str(simvol)

        pokazat()

    # -----------------------------
    # Кнопки
    # -----------------------------

    vse_knopki = [

        ("AC", "AC", "#ef5350"),
        ("C", "C", "#F8BBD0"),
        ("(", "(", "#F8BBD0"),
        (")", ")", "#F8BBD0"),

        ("sin", "sin", "#F8BBD0"),
        ("cos", "cos", "#F8BBD0"),
        ("tan", "tan", "#F8BBD0"),
        ("√", "√", "#F8BBD0"),

        ("7", "7", "#424242"),
        ("8", "8", "#424242"),
        ("9", "9", "#424242"),
        ("÷", "÷", "#F8BBD0"),

        ("4", "4", "#424242"),
        ("5", "5", "#424242"),
        ("6", "6", "#424242"),
        ("×", "×", "#F8BBD0"),

        ("1", "1", "#424242"),
        ("2", "2", "#424242"),
        ("3", "3", "#424242"),
        ("-", "-", "#F8BBD0"),

        ("0", "0", "#424242"),
        (".", ".", "#424242"),
        ("=", "=", "#43a047"),
        ("+", "+", "#F8BBD0"),
    ]

    # -----------------------------
    # Создание кнопок
    # -----------------------------

    buttons = []

    for label, data, color in vse_knopki:

        text_color = (
            "#263238"
            if color == "#FFD54F"
            else ft.Colors.WHITE
        )

        button = ft.Button(
            content=ft.Text(
                value=label,
                size=16 if len(label) > 1 else 20,
                weight=ft.FontWeight.BOLD,
                color=text_color,
            ),
            data=data,
            on_click=knopka_nazhata,
            bgcolor=color,
            height=58,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=10
                ),
            ),
        )

        buttons.append(button)

    # -----------------------------
    # Строки кнопок
    # -----------------------------

    rows = []

    for i in range(0, len(buttons), 4):

        rows.append(
            ft.Row(
                buttons[i:i + 4],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=7,
            )
        )

    # -----------------------------
    # Окно калькулятора
    # -----------------------------

    kalkulyator = ft.Container(
        content=ft.Column(
            [
                ekran,

                ft.Divider(
                    height=4,
                    color=ft.Colors.TRANSPARENT,
                ),

                *rows,
            ],

            spacing=7,

            horizontal_alignment=(
                ft.CrossAxisAlignment.CENTER
            ),
        ),

        padding=16,

        bgcolor="#263238",

        border_radius=18,

        border=ft.Border.all(
            1,
            "#455a64",
        ),

        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            offset=ft.Offset(4, 6),
        ),
    )

    # -----------------------------
    # Служба поддержки
    # -----------------------------

    podderzhka = ft.Text(
        value="СЛУЖБА ПОДДЕРЖКИ: __________________",
        size=14,
        color="#555555",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # -----------------------------
    # Основной экран
    # -----------------------------

    root = ft.Column(
        [
            welcome_ru,

            welcome_en,

            ft.Container(height=12),

            kalkulyator,

            ft.Container(height=10),

            podderzhka,
        ],

        horizontal_alignment=(
            ft.CrossAxisAlignment.CENTER
        ),

        spacing=0,
    )

    page.add(root)

    # -----------------------------
    # Адаптация под телефон
    # -----------------------------

    def adapt_layout(e=None):

        width = page.width or 380

        # Максимальная ширина на компьютере
        # и автоматическое уменьшение на телефоне.
        calc_width = min(
            380,
            max(280, width - 24),
        )

        kalkulyator.width = calc_width

        ekran.width = calc_width - 32

        inner_width = calc_width - 32

        button_width = (
            inner_width - 21
        ) / 4

        for button in buttons:
            button.width = button_width

        # На маленьком экране уменьшаем дисплей.
        if calc_width < 330:
            rezultat.size = 27
            ekran.height = 78
        else:
            rezultat.size = 32
            ekran.height = 90

        page.update()

    page.on_resize = adapt_layout

    adapt_layout()


# Запуск как ASGI-приложение для Render
app = ft.run(main, export_asgi_app=True)
