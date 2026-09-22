import math
import cmath
import re
import flet as ft

def main(page: ft.Page):
    page.title = "Математический калькулятор"
    page.bgcolor = ft.Colors.WHITE
    page.padding = 12
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    stroka = {"value": ""}

    welcome_ru = ft.Text(
        value="Добро пожаловать",
        size=24,
        color="#263238",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER)

    welcome_en = ft.Text(
        value="Welcome",
        size=18,
        color="#555555",
        text_align=ft.TextAlign.CENTER)

    rezultat = ft.Text(
        value="0",
        size=32,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.RIGHT,
        weight=ft.FontWeight.BOLD)

    ekran = ft.Container(
        content=ft.Row(
            [rezultat],
            alignment=ft.MainAxisAlignment.END),
        bgcolor="#171717",
        padding=15,
        height=90,
        border_radius=12)

    def sin_deg(x):
        return cmath.sin(x * math.pi / 180)

    def cos_deg(x):
        return cmath.cos(x * math.pi / 180)

    def tan_deg(x):
        angle = x * math.pi / 180

        if abs(cmath.cos(angle)) < 1e-12:
            raise ValueError("Тангенс не существует")

        return cmath.tan(angle)

    def sqrt_func(x):
        return cmath.sqrt(x)

    def pokazat(tekst=None):
        if tekst is None:
            tekst = stroka["value"]

        if not tekst:
            rezultat.value = "0"
        else:
            rezultat.value = tekst.replace("sqrt(", "√(")

        page.update()

    def podgotovit_complex(primer):
        primer = primer.replace(" ", "")

        if re.search(r"[^0-9+\-*/().a-zA-Z×÷i]", primer):
            raise ValueError("Недопустимые символы")

        primer = re.sub(
            r"(?<![a-zA-Z])i(?![a-zA-Z])",
            "j",
            primer)

        return primer

    def vychislit(primer):
        primer = primer.replace("×", "*")
        primer = primer.replace("÷", "/")
        primer = podgotovit_complex(primer)

        proverka = (
            primer
            .replace("sin", "")
            .replace("cos", "")
            .replace("tan", "")
            .replace("sqrt", "")
            .replace("j", ""))

        razresheno = set("0123456789.+-*/()")

        if not set(proverka).issubset(razresheno):
            raise ValueError("Недопустимые символы")

        bezopasno = {"__builtins__": {},"sin": sin_deg,"cos": cos_deg,"tan": tan_deg,"sqrt": sqrt_func,"j": 1j}

        return eval(primer, bezopasno, {})

    def krasivoe_chislo(value):
        if isinstance(value, complex):
            real = value.real
            imag = value.imag

            if abs(real) < 1e-12:
                real = 0
            if abs(imag) < 1e-12:
                imag = 0
            if imag == 0:
                return f"{real:g}"
            if real == 0:
                if abs(imag - 1) < 1e-12:
                    return "i"
                if abs(imag + 1) < 1e-12:
                    return "-i"
                return f"{imag:g}i"

            sign = "+" if imag >= 0 else "-"

            if abs(abs(imag) - 1) < 1e-12:
                imag_text = "i"
            else:
                imag_text = f"{abs(imag):g}i"
            return f"{real:g} {sign} {imag_text}"

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

            otkrytye = primer.count("(")
            zakrytye = primer.count(")")

            if otkrytye > zakrytye:
                primer += ")" * (otkrytye - zakrytye)

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

    def dobavit_funkciyu(name):
        if stroka["value"] == "0":
            stroka["value"] = ""

        stroka["value"] += f"{name}("
        pokazat()

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

    vse_knopki = [
        ("AC", "AC", "#EF5350"),
        ("C", "C", "#F8BBD0"),
        ("(", "(", "#F8BBD0"),
        (")", ")", "#F8BBD0"),
        ("sin", "sin", "#F8BBD0"),
        ("cos", "cos", "#F8BBD0"),
        ("tan", "tan", "#F8BBD0"),
        ("√", "√", "#F8BBD0"),
        ("i", "i", "#F8BBD0"),
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
        ("=", "=", "#43A047"),
        ("+", "+", "#F8BBD0")]

    buttons = []

    for label, data, color in vse_knopki:
        if color == "#F8BBD0":
            text_color = "#263238"
        else:
            text_color = ft.Colors.WHITE

        if label in ("sin", "cos", "tan"):
            text_size = 11
        elif len(label) > 1:
            text_size = 14
        else:
            text_size = 20

        button = ft.Button(
            content=ft.Text(
                value=label,
                size=text_size,
                weight=ft.FontWeight.BOLD,
                color=text_color,
                no_wrap=True),
            data=data,
            on_click=knopka_nazhata,
            bgcolor=color,
            height=58,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)))

        buttons.append(button)

    rows = []

    rows.append(ft.Row(
        buttons[0:4],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=7))

    rows.append(ft.Row(
        buttons[4:9],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5))

    rows.append(ft.Row(
        buttons[9:13],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=7))

    rows.append(ft.Row(
        buttons[13:17],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=7))

    rows.append(ft.Row(
        buttons[17:21],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=7))

    rows.append(ft.Row(
        buttons[21:25],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=7))

    kalkulyator = ft.Container(
        content=ft.Column(
            [ekran,ft.Divider(height=4,color=ft.Colors.TRANSPARENT),*rows],
            spacing=7,horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=16,bgcolor="#263238",
        border_radius=18,
        border=ft.Border.all(1,"#455A64"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            offset=ft.Offset(4, 6)))

    podderzhka = ft.Column([
        ft.Text("Email: calcut_helper@mail.ru", size=11, color="#555555", weight=ft.FontWeight.BOLD, no_wrap=True),
        ft.Text("Support: @calc_support_bot", size=11, color="#555555", weight=ft.FontWeight.BOLD, no_wrap=True),
        ft.Text("Тех. поддержка: @calc_support_bot", size=11, color="#555555", weight=ft.FontWeight.BOLD, no_wrap=True)], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    root = ft.Column([welcome_ru,
            welcome_en,
            ft.Container(height=12),
            kalkulyator,
            ft.Container(height=10),
            podderzhka],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0)

    page.add(root)

    def adapt_layout(e=None):
        width = page.width or 380

        calc_width = min(
            380,
            max(280, width - 24))

        kalkulyator.width = calc_width
        ekran.width = calc_width - 32

        inner_width = calc_width - 32

        normal_button_width = (inner_width - 21) / 4
        function_button_width = (inner_width - 20) / 5

        for button in buttons:
            button.width = normal_button_width

        for button in buttons[4:9]:
            button.width = function_button_width

        if calc_width < 330:
            rezultat.size = 27
            ekran.height = 78
        else:
            rezultat.size = 32
            ekran.height = 90

        page.update()

    page.on_resize = adapt_layout
    adapt_layout()

app = ft.run(main, export_asgi_app=True)
