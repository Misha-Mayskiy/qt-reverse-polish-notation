from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel,
                               QTextEdit, QListWidget, QGridLayout, QGroupBox,
                               QSplitter, QMessageBox, QListWidgetItem, QStatusBar,
                               QMenuBar, QMenu, QGraphicsDropShadowEffect, QCompleter)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal, QRect, QTimer, QStringListModel
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QColor, QKeySequence, QShortcut, QAction
import sys
from rpn_calculator.parser import parse_str_infix, is_infix, parse_str_postfix
from rpn_calculator.calculator import rpn_calculator


class AnimatedButton(QPushButton):
    """Кнопка с улучшенной анимацией"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.default_style = ""
        self.hover_style = ""
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._animate_pulse)
        self.pulse_count = 0

        # Эффект тени
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        # Увеличиваем тень при наведении
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 4)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращаем тень к исходному состоянию
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 2)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        # Убираем тень при нажатии
        self.shadow.setBlurRadius(5)
        self.shadow.setOffset(0, 1)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Возвращаем тень после отпускания
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 2)
        # Запускаем анимацию пульсации
        self.pulse_count = 0
        self._animation_timer.start(50)
        super().mouseReleaseEvent(event)

    def _animate_pulse(self):
        """Анимация пульсации после клика"""
        self.pulse_count += 1
        if self.pulse_count > 10:
            self._animation_timer.stop()
            self.shadow.setColor(QColor(0, 0, 0, 80))
            return

        # Изменяем цвет тени для эффекта пульсации
        alpha = 80 + (20 * (1 - self.pulse_count / 10))
        self.shadow.setColor(QColor(100, 200, 255, int(alpha)))


class CalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.env = {}
        self.history = []
        self.last_result = None
        self.history_visible = True
        self.init_ui()
        self.apply_styles()
        self.create_menu_bar()
        self.create_status_bar()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Modern RPN/Infix Calculator")
        self.setGeometry(100, 100, 900, 700)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Левая панель с калькулятором
        left_panel = self.create_calculator_panel()

        # Правая панель с историей и переменными
        self.right_panel = self.create_info_panel()

        # Splitter для изменения размеров панелей
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

        # Горячие клавиши
        self.setup_shortcuts()

    def create_menu_bar(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        clear_action = QAction("Очистить все", self)
        clear_action.setShortcut("Ctrl+Shift+C")
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Правка
        edit_menu = menubar.addMenu("Правка")

        copy_result_action = QAction("Копировать результат", self)
        copy_result_action.setShortcut("Ctrl+R")
        copy_result_action.triggered.connect(self.copy_result)
        edit_menu.addAction(copy_result_action)

        # Меню Вид
        view_menu = menubar.addMenu("Вид")

        self.toggle_history_action = QAction("Показать/скрыть историю", self)
        self.toggle_history_action.setShortcut("Ctrl+H")
        self.toggle_history_action.triggered.connect(self.toggle_history)
        view_menu.addAction(self.toggle_history_action)

    def create_status_bar(self):
        """Создание статус-бара"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к вычислениям")

    def create_calculator_panel(self):
        """Создание панели калькулятора"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # Дисплей
        display_group = QGroupBox("ВЫЧИСЛЕНИЯ")
        display_layout = QVBoxLayout()
        display_layout.setSpacing(10)

        # Поле ввода с автодополнением
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите выражение...")
        self.input_field.setFont(QFont("Consolas", 14))
        self.input_field.returnPressed.connect(self.calculate)
        self.input_field.textChanged.connect(self.on_input_changed)

        # Добавляем автодополнение для переменных
        self.completer = QCompleter()
        self.input_field.setCompleter(self.completer)

        display_layout.addWidget(self.input_field)

        # Результат (теперь можно выделять и копировать)
        self.result_label = QLineEdit("= 0")
        self.result_label.setReadOnly(True)
        self.result_label.setFont(QFont("Consolas", 18, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignRight)
        self.result_label.setMinimumHeight(50)
        self.result_label.setContextMenuPolicy(Qt.DefaultContextMenu)  # Включаем контекстное меню
        display_layout.addWidget(self.result_label)

        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        # Кнопки
        buttons_group = QGroupBox("КЛАВИАТУРА")
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(8)

        # Определение кнопок с эмодзи
        buttons = [
            # Ряд 0
            [('C', 'clear', '🗑️'), ('(', 'operator', None), (')', 'operator', None), ('⌫', 'clear', None)],
            # Ряд 1
            [('sin', 'function', None), ('cos', 'function', None), ('tan', 'function', None),
             ('sqrt', 'function', '√')],
            # Ряд 2
            [('7', 'number', None), ('8', 'number', None), ('9', 'number', None), ('/', 'operator', '÷')],
            # Ряд 3
            [('4', 'number', None), ('5', 'number', None), ('6', 'number', None), ('*', 'operator', '×')],
            # Ряд 4
            [('1', 'number', None), ('2', 'number', None), ('3', 'number', None), ('-', 'operator', None)],
            # Ряд 5
            [('0', 'number', None), ('.', 'number', None), ('^', 'operator', None), ('+', 'operator', None)],
            # Ряд 6
            [('log', 'function', None), ('ln', 'function', None), ('π', 'constant', None), ('=', 'equals', None)]
        ]

        # Создание кнопок
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_data in enumerate(row):
                text, btn_type = btn_data[0], btn_data[1]
                icon = btn_data[2] if len(btn_data) > 2 else None

                btn = AnimatedButton(icon if icon else text)
                btn.setMinimumHeight(50)
                btn.setFont(QFont("Arial", 14, QFont.Bold))
                btn.clicked.connect(lambda checked, t=text: self.button_click(t))

                # Применение стилей в зависимости от типа
                btn.setProperty("button_type", btn_type)

                # Добавляем tooltip
                if text in ['sin', 'cos', 'tan']:
                    btn.setToolTip(f"Тригонометрическая функция {text}")
                elif text == 'sqrt':
                    btn.setToolTip("Квадратный корень")
                elif text == 'log':
                    btn.setToolTip("Логарифм по основанию 10")
                elif text == 'ln':
                    btn.setToolTip("Натуральный логарифм")
                elif text == 'π':
                    btn.setToolTip("Константа π (3.14159...)")

                buttons_layout.addWidget(btn, row_idx, col_idx)

        buttons_group.setLayout(buttons_layout)
        layout.addWidget(buttons_group)

        return panel

    def create_info_panel(self):
        """Создание информационной панели"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # История
        self.history_group = QGroupBox("ИСТОРИЯ ВЫЧИСЛЕНИЙ")
        history_layout = QVBoxLayout()

        self.history_list = QListWidget()
        self.history_list.setFont(QFont("Consolas", 11))
        self.history_list.itemDoubleClicked.connect(self.use_history_item)
        history_layout.addWidget(self.history_list)

        # Кнопка очистки истории
        clear_history_btn = QPushButton("Очистить историю")
        clear_history_btn.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_history_btn)

        self.history_group.setLayout(history_layout)
        layout.addWidget(self.history_group, 2)

        # Переменные
        vars_group = QGroupBox("ПЕРЕМЕННЫЕ")
        vars_layout = QVBoxLayout()

        self.vars_text = QTextEdit()
        self.vars_text.setFont(QFont("Consolas", 11))
        self.vars_text.setReadOnly(True)
        self.vars_text.setMaximumHeight(200)
        vars_layout.addWidget(self.vars_text)

        # Кнопка очистки переменных
        clear_vars_btn = QPushButton("Очистить переменные")
        clear_vars_btn.clicked.connect(self.clear_variables)
        vars_layout.addWidget(clear_vars_btn)

        vars_group.setLayout(vars_layout)
        layout.addWidget(vars_group, 1)

        return panel

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Ctrl+H - показать/скрыть историю
        QShortcut(QKeySequence("Ctrl+H"), self, self.toggle_history)
        # Ctrl+L - очистить
        QShortcut(QKeySequence("Ctrl+L"), self, self.clear_input)
        # Escape - очистить
        QShortcut(QKeySequence("Escape"), self, self.clear_input)

    def on_input_changed(self, text):
        """Обновление автодополнения при изменении текста"""
        # Обновляем список переменных для автодополнения
        var_list = list(self.env.keys())
        self.completer.setModel(QStringListModel(var_list))

    def button_click(self, text):
        """Обработка нажатия кнопки"""
        current = self.input_field.text()

        if text == 'C' or text == '🗑️':
            self.clear_input()
        elif text == '⌫':
            self.input_field.setText(current[:-1])
        elif text == '=':
            self.calculate()
        elif text == 'π':
            if current and not current.endswith(' '):
                self.input_field.insert(' pi')
            else:
                self.input_field.insert('pi')
        else:
            # Добавляем пробелы для операторов
            if text in ['+', '-', '*', '/', '^']:
                if current and current[-1] != ' ':
                    self.input_field.insert(f' {text} ')
                else:
                    self.input_field.insert(f'{text} ')
            elif text in ['sin', 'cos', 'tan', 'sqrt', 'log', 'ln']:
                self.input_field.insert(f'{text}(')
            else:
                self.input_field.insert(text)

        self.input_field.setFocus()

    def calculate(self):
        """Вычисление выражения"""
        expression = self.input_field.text().strip()
        if not expression:
            return

        try:
            # Проверка на присваивание
            var_name = None
            if '=' in expression:
                parts = expression.split('=', 1)
                var_name = parts[0].strip()
                expression = parts[1].strip()
                if not var_name.isidentifier():
                    raise ValueError(f"Недопустимое имя переменной: {var_name}")

            # Парсинг и вычисление
            rpn_expr = parse_str_infix(expression) if is_infix(expression) else parse_str_postfix(expression)
            result = rpn_calculator(rpn_expr, self.env)
            self.last_result = result

            # Обновление интерфейса
            if var_name:
                self.env[var_name] = result
                self.result_label.setText(f"{var_name} = {result}")
                self.add_to_history(f"{var_name} = {expression} = {result}")
                self.update_variables_display()
            else:
                self.result_label.setText(f"= {result}")
                self.add_to_history(f"{expression} = {result}")

            # Анимация результата
            self.animate_result(success=True)

            # Обновляем статус
            self.status_bar.showMessage("Вычисление выполнено успешно", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.result_label.setText("Ошибка!")
            self.animate_result(success=False)
            self.status_bar.showMessage(f"Ошибка: {str(e)}", 5000)

    def add_to_history(self, item):
        """Добавление в историю"""
        list_item = QListWidgetItem(item)
        self.history_list.insertItem(0, list_item)
        self.history.insert(0, item)

        # Ограничение истории
        while self.history_list.count() > 100:
            self.history_list.takeItem(100)
            self.history.pop()

    def use_history_item(self, item):
        """Использование элемента истории"""
        text = item.text()
        if '=' in text:
            # Берем выражение до первого знака равенства
            expr = text.split('=')[0].strip()
            self.input_field.setText(expr)
            self.input_field.setFocus()

    def update_variables_display(self):
        """Обновление отображения переменных"""
        if not self.env:
            self.vars_text.setText("Нет сохраненных переменных")
        else:
            vars_text = "\n".join([f"{k} = {v}" for k, v in sorted(self.env.items())])
            self.vars_text.setText(vars_text)

    def clear_variables(self):
        """Очистка переменных"""
        if not self.env:
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Очистить все переменные ({len(self.env)} шт.)?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.env.clear()
            self.update_variables_display()
            self.status_bar.showMessage("Все переменные очищены", 3000)

    def clear_history(self):
        """Очистка истории"""
        if self.history_list.count() == 0:
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     f"Очистить историю ({self.history_list.count()} записей)?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history_list.clear()
            self.history.clear()
            self.status_bar.showMessage("История очищена", 3000)

    def clear_input(self):
        """Очистка ввода"""
        self.input_field.clear()
        self.result_label.setText("= 0")
        self.last_result = None
        self.status_bar.showMessage("Готов к вычислениям")

    def clear_all(self):
        """Очистка всего"""
        reply = QMessageBox.question(self, "Подтверждение",
                                     "Очистить все данные (историю, переменные, ввод)?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_input()
            self.history_list.clear()
            self.history.clear()
            self.env.clear()
            self.update_variables_display()
            self.status_bar.showMessage("Все данные очищены", 3000)

    def copy_result(self):
        """Копирование результата в буфер обмена"""
        if self.last_result is not None:
            QApplication.clipboard().setText(str(self.last_result))
            self.status_bar.showMessage("Результат скопирован в буфер обмена", 3000)

    def toggle_history(self):
        """Переключение видимости истории"""
        if self.history_visible:
            # Скрываем историю
            self.history_group.hide()
            self.history_visible = False
            self.status_bar.showMessage("История скрыта", 2000)
            # Изменяем размеры splitter'а
            sizes = self.splitter.sizes()
            self.splitter.setSizes([sizes[0] + sizes[1] // 2, sizes[1] // 2])
        else:
            # Показываем историю
            self.history_group.show()
            self.history_visible = True
            self.status_bar.showMessage("История показана", 2000)
            # Восстанавливаем размеры
            total = sum(self.splitter.sizes())
            self.splitter.setSizes([total * 2 // 3, total // 3])

    def animate_result(self, success=True):
        """Анимация результата"""
        # Создаем эффект свечения для результата
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)

        if success:
            glow.setColor(QColor(76, 175, 80, 180))  # Зеленое свечение
        else:
            glow.setColor(QColor(244, 67, 54, 180))  # Красное свечение

        self.result_label.setGraphicsEffect(glow)

        # Убираем эффект через некоторое время
        QTimer.singleShot(1000, lambda: self.result_label.setGraphicsEffect(None))

    def apply_styles(self):
        """Применение стилей"""
        style = """
        QMainWindow {
            background-color: #1a1a1a;
        }

        QGroupBox {
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            border: 2px solid #444444;
            border-radius: 12px;
            margin-top: 15px;
            padding-top: 15px;
            background-color: #252525;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 5px 20px;
            background-color: #333333;
            border-radius: 6px;
            letter-spacing: 1px;
        }

        QLineEdit {
            background-color: #2d2d2d;
            border: 2px solid #3a3a3a;
            border-radius: 8px;
            padding: 10px;
            color: #ffffff;
            font-size: 15px;
            selection-background-color: #4fc3f7;
        }

        QLineEdit:focus {
            border-color: #4fc3f7;
            background-color: #333333;
        }

        QLineEdit[readOnly="true"] {
            color: #4fc3f7;
            background-color: #2d2d2d;
            border: 2px solid #3a3a3a;
            border-radius: 8px;
            padding: 10px;
        }

        QPushButton {
            background-color: #3a3a3a;
            border: none;
            border-radius: 8px;
            color: white;
            padding: 10px;
            font-weight: bold;
            min-height: 25px;
        }

        QPushButton:hover {
            background-color: #4a4a4a;
        }

        QPushButton:pressed {
            background-color: #2a2a2a;
            padding: 11px 9px 9px 11px;
        }

        QPushButton[button_type="number"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #4a4a4a, stop: 1 #3a3a3a);
        }

        QPushButton[button_type="number"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #5a5a5a, stop: 1 #4a4a4a);
        }

        QPushButton[button_type="operator"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #ff7b45, stop: 1 #ff5b25);
        }

        QPushButton[button_type="operator"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #ff9b65, stop: 1 #ff7b45);
        }

        QPushButton[button_type="function"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #8c5dff, stop: 1 #6c3dff);
        }

        QPushButton[button_type="function"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #ac7dff, stop: 1 #8c5dff);
        }

        QPushButton[button_type="equals"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #10d863, stop: 1 #00b843);
            font-size: 18px;
        }

        QPushButton[button_type="equals"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #30f883, stop: 1 #10d863);
        }

        QPushButton[button_type="clear"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #ff4848, stop: 1 #ff2828);
        }

        QPushButton[button_type="clear"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #ff6868, stop: 1 #ff4848);
        }

        QPushButton[button_type="constant"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #31a6f3, stop: 1 #1186d3);
        }

        QPushButton[button_type="constant"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #51c6f3, stop: 1 #31a6f3);
        }

        QListWidget {
            background-color: #2d2d2d;
            border: 2px solid #3a3a3a;
            border-radius: 8px;
            color: #e0e0e0;
            padding: 8px;
            outline: none;
        }

        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #3a3a3a;
            border-radius: 4px;
            margin: 2px;
        }

        QListWidget::item:hover {
            background-color: #3a3a3a;
        }

        QListWidget::item:selected {
            background-color: #4fc3f7;
            color: #1a1a1a;
        }

        QTextEdit {
            background-color: #2d2d2d;
            border: 2px solid #3a3a3a;
            border-radius: 8px;
            color: #e0e0e0;
            padding: 8px;
            font-family: Consolas, monospace;
        }

        QSplitter::handle {
            background-color: #3a3a3a;
            width: 3px;
            border-radius: 1px;
        }

        QSplitter::handle:hover {
            background-color: #4fc3f7;
        }

        QStatusBar {
            background-color: #242424;
            color: #a0a0a0;
            border-top: 1px solid #3a3a3a;
            font-size: 12px;
        }

        QMenuBar {
            background-color: #242424;
            color: #e0e0e0;
            border-bottom: 1px solid #3a3a3a;
        }

        QMenuBar::item:selected {
            background-color: #3a3a3a;
        }

        QMenu {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
        }

        QMenu::item:selected {
            background-color: #4fc3f7;
            color: #1a1a1a;
        }

        QMessageBox {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        """
        self.setStyleSheet(style)


def run_gui():
    """Запуск GUI приложения"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Установка темной темы
    app.setStyle("Fusion")

    # Настройка темной палитры
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(26, 26, 26))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    calculator = CalculatorGUI()
    calculator.show()

    sys.exit(app.exec())
