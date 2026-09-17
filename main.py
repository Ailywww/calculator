import math
import cmath
import flet as ft


def main(page: ft.Page):
    # =========================================================
    # НАСТРОЙКИ СТРАНИЦЫ
    # =========================================================
    page.title = "Математический калькулятор"
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # =========================================================
    # ЭКРАН
    # =========================================================
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
        width=340,
        border_radius=12,
    )

    # Внутреннее выражение хранится здесь.
    # Например: sqrt(sin(30))
    stroka = {"value": ""}

    def pokazat(tekst=None):
        """Показывает выражение на экране."""
        if tekst is None:
            tekst = stroka["value"]

        if not tekst:
            rezultat.value = "0"
        else:
            # Внутри используем sqrt(...), пользователю показываем √(...)
            rezultat.value = tekst.replace("sqrt(", "√(")

        page.update()

    # =========================================================
    # ТРИГОНОМЕТРИЯ В ГРАДУСАХ
    # =========================================================
    def sin_deg(x):
        return math.sin(math.radians(x))

    def cos_deg(x):
        return math.cos(math.radians(x))

    def tan_deg(x):
        if abs(math.cos(math.radians(x))) < 1e-12:
            raise ValueError("Тангенс не существует")
        return math.tan(math.radians(x))

    # =========================================================
    # КОРЕНЬ
    # =========================================================
    def sqrt_func(x):
        if x < 0:
            return cmath.sqrt(complex(x, 0))
        return math.sqrt(x)

    # =========================================================
    # ВЫЧИСЛЕНИЕ
    # =========================================================
    def vychislit(primer):
        primer = primer.replace("×", "*").replace("÷", "/")

        # Разрешаем только наши функции и математические символы.
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

        # eval используется только с белым списком функций
        # и отключёнными встроенными функциями Python.
        bezopasno = {
            "__builtins__": {},
            "sin": sin_deg,
            "cos": cos_deg,
            "tan": tan_deg,
            "sqrt": sqrt_func,
        }

        return eval(primer, bezopasno, {})

    # =========================================================
    # КРАСИВЫЙ ВЫВОД
    # =========================================================
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

    # =========================================================
    # ДОБАВЛЕНИЕ ФУНКЦИИ
    # =========================================================
    def dobavit_funkciyu(name):
        if stroka["value"] == "0":
            stroka["value"] = ""

        stroka["value"] += f"{name}("
        pokazat()

    # =========================================================
    # ОБРАБОТКА КНОПОК
    # =========================================================
    def knopka_nazhata(e):
        simvol = e.control.data

        if simvol == "AC":
            stroka["value"] = ""
            pokazat()
            return

        if simvol == "C":
            stroka["value"] = stroka["value"][:-1]
            pokazat()
            return

        if simvol in ("sin", "cos", "tan"):
            dobavit_funkciyu(simvol)
            return

        if simvol == "√":
            if stroka["value"] == "0":
                stroka["value"] = ""
            stroka["value"] += "sqrt("
            pokazat()
            return

        if simvol == "=":
            poschitat()
            return

        if stroka["value"] == "0":
            stroka["value"] = ""

        stroka["value"] += str(simvol)
        pokazat()

    # =========================================================
    # КНОПКИ
    # =========================================================
    vse_knopki = [
        ("AC", "AC", "#ef5350"),
        ("C", "C", "#ff9800"),
        ("(", "(", "#78909c"),
        (")", ")", "#78909c"),

        ("sin", "sin", "#8e44ad"),
        ("cos", "cos", "#8e44ad"),
        ("tan", "tan", "#8e44ad"),
        ("√", "√", "#8e44ad"),

        ("7", "7", "#37474f"),
        ("8", "8", "#37474f"),
        ("9", "9", "#ff9800"),
        ("÷", "÷", "#ff9800"),

        ("4", "4", "#37474f"),
        ("5", "5", "#37474f"),
        ("6", "6", "#37474f"),
        ("×", "×", "#ff9800"),

        ("1", "1", "#37474f"),
        ("2", "2", "#37474f"),
        ("3", "3", "#37474f"),
        ("-", "-", "#ff9800"),

        ("0", "0", "#37474f"),
        (".", ".", "#37474f"),
        ("=", "=", "#43a047"),
        ("+", "+", "#ff9800"),
    ]

    rows = []

    for i in range(0, len(vse_knopki), 4):
        row_buttons = []

        for label, data, color in vse_knopki[i:i + 4]:
            button = ft.Button(
                content=ft.Text(
                    value=label,
                    size=16 if len(label) > 1 else 20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                data=data,
                on_click=knopka_nazhata,
                bgcolor=color,
                width=75,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            )
            row_buttons.append(button)

        rows.append(
            ft.Row(
                row_buttons,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            )
        )

    # =========================================================
    # ОКНО КАЛЬКУЛЯТОРА
    # =========================================================
    kalkulyator = ft.Container(
        content=ft.Column(
            [
                ekran,
                ft.Divider(
                    height=10,
                    color=ft.Colors.TRANSPARENT,
                ),
                *rows,
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#263238",
        width=380,
        padding=20,
        border_radius=18,
        border=ft.Border.all(1, "#455a64"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            offset=ft.Offset(4, 6),
        ),
    )

    # =========================================================
    # ТЕЛЕФОН ГОРЯЧЕЙ ЛИНИИ
    # =========================================================
    telefon = ft.Text(
        value="ТЕЛЕФОН ГОРЯЧЕЙ ЛИНИИ: __________________",
        size=16,
        color="#555555",
        weight=ft.FontWeight.BOLD,
    )

    # =========================================================
    # РАЗМЕЩЕНИЕ
    # =========================================================
    page.add(
        ft.Stack(
            [
                ft.Container(
                    content=kalkulyator,
                    left=80,
                    top=40,
                ),
                ft.Container(
                    content=telefon,
                    right=25,
                    bottom=20,
                ),
            ],
            expand=True,
        )
    )


# =============================================================
# ЗАПУСК
# =============================================================
# Для Render это ASGI-приложение.
# Render запустит его через Uvicorn.
app = ft.run(main, export_asgi_app=True)
