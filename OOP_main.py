from tabulate import tabulate

class AutoCatalog:

    def __init__(self, file_name = r'C:\lab with git\oop_cars_tests\auto_oop.txt'):
        self.file_name = file_name

    def _read_catalog(self):
        with open(self.file_name, 'r', encoding='UTF-8') as file:
            lines = file.readlines()
        return [line.strip().split(',') for line in lines]

    def _get_valid_input(self):
        while True:
            user_input = input()
            if user_input.isdigit():
                return user_input
            else:
                print('Вы ввели не число! Попробуйте снова:')

    def _line_warning(self, lines):
        while True:
            user_input = input()
            if user_input.isdigit():
                if int(user_input) == 0 or int(user_input) > (len(lines) - 1):
                    print('Ошибка: такое число отсутствует! Попробуйте заново:')
                else:
                    return user_input
            else:
                print('Вы ввели не число! Попробуйте снова')

    def _get_car_by_number(self, str_number, lines):
        res = []
        res.append(self._get_header_row(lines))
        num = int(str_number)
        row = lines[num]
        res.append(row)
        return res

    def show_catalog(self):
        lines = self._read_catalog()
        table = tabulate(lines, headers="firstrow", tablefmt="grid")
        print(table)
        print('Введите номер машины в списке:')
        str_number = self._line_warning(lines)
        car = self._get_car_by_number(str_number, lines)
        table = tabulate(car, headers="firstrow", tablefmt="grid")
        print(table)


    def show_all(self):
        catalog = self._read_catalog()
        table = tabulate(catalog, headers="firstrow", tablefmt="grid")
        print(table)

    def _get_header_row(self, lines):
        return lines[0]

    def add_car(self):
        lines = self._read_catalog()
        row = self._get_header_row(lines)
        new_line = self._get_new_car_row(lines, row)
        lines.append(new_line)
        self._write_catalog(lines)

    def search_car(self):
        print('Введите "1" если по фирме')
        print('Введите "2" если по моделе')
        print('Введите "3" если по номеру')
        search_by = self._get_valid_input()
        lines = self._read_catalog()

        if not lines[1:]:
            print('Ошибка : В базе нет машин!')
            return

        if search_by == '1':
            print('Введите фирму:')
            search_value = input()
            catalog = self._search_by_firm(lines, search_value)
            self._display_search_result(catalog)

        elif search_by == '2':
            print('Введите модель:')
            search_value = input()
            catalog = self._search_by_model(lines, search_value)
            self._display_search_result(catalog)

        elif search_by == '3':
            print('Введите номер:')
            search_value = input()
            catalog = self._search_by_number(lines, search_value)
            self._display_search_result(catalog)

        else:
            print('Неподходящее значение! Попробуйте заново\n')

    def delete_car(self):
        lines = self._read_catalog()
        print('Введите номер машины в списке:')
        str_number = self._get_valid_input()
        if int(str_number) == 0 or int(str_number) > (len(lines) - 1):
            print('Ошибка : такое число отсутсвтует! Попробуй заново\n')
        else:
            line_to_del = self._find_line_to_delete(lines, str_number)
            del lines[line_to_del]

            self._update_line_numbers(lines)

    def update_car(self):
        lines = self._read_catalog()
        print('Введите номер машины в списке:')
        str_number = self._get_valid_input()
        if int(str_number) == 0 or int(str_number) > (len(lines) - 1):
            print('Ошибка : такое число отсутсвтует! Попробуй заново\n')
        else:
            print('Введите название параметра:')
            res = []
            res.append(self._get_header_row(lines))
            while True:
                name_parameter = input()
                if name_parameter not in res[0]:
                    print('Неизвестное имя параметра! Попробуйте вновь:\n')
                else:
                    break
            print('Новая характеристика:')
            new_parameter = input()
            number_parameter = res[0].index(name_parameter)
            num = int(str_number)
            lines[num][number_parameter] = new_parameter

            self._write_catalog(lines)


    def _write_catalog(self, lines):
        with open(self.file_name, 'w', encoding='UTF-8') as file:
            file.writelines(','.join(map(str, line)) + '\n' for line in lines[:-1])
            file.writelines(','.join(map(str, lines[-1])))

    def _get_new_car_row(self, lines, header_row):
        new_row = [str(len(lines))]  # Start with the line number
        for element in header_row[1:]:
            param = self._get_user_input_for_param(element)
            new_row.append(param)

        return new_row

    def _get_user_input_for_param(self, element):
        if element[-1] == '?':
            while True:
                print(f'{element} (Да или Нет):')
                param = input()
                if param == 'Да' or param == 'Нет':
                    return param
                else:
                    print('Неподходящее значение! Попробуйте заново\n')
        else:
            while True:
                print(f'{element}:')
                param = input()
                if len(param) > 0:
                    return param
                else:
                    print('Неподходящее значение! Попробуйте заново\n')

    def _search_by_firm(self, lines, firm):
        catalog = [row for row in lines if row[1] == firm or row[1] == 'Фирма']
        return catalog

    def _search_by_model(self, lines, model):
        catalog = [row for row in lines if row[2] == model or row[2] == 'Модель']
        return catalog

    def _search_by_number(self, lines, number):
        catalog = [row for row in lines if row[3] == number or row[3] == 'Номер']
        return catalog

    def _display_search_result(self, catalog):
        table = tabulate(catalog, headers="firstrow", tablefmt="grid")
        print(table)

    def _find_line_to_delete(self, lines, str_number):
        for line in range(1,len(lines)):
            if lines[line][0] == str_number or (lines[line][0] + lines[line][1]) == str_number:
                return line

    def _update_line_numbers(self, lines):
        res = []
        res.append(self._get_header_row(lines))
        for line in range(1, len(lines)):
            lines[line][0] = str(line)
            new_line = lines[line]
            res.append(new_line)
        self._write_catalog(res)

    def check_new_par(self):
        while True:
            par = input('Введите новый параметр:\n')
            if par == '' or par.count(' ') == len(par):
                print('Введена пустая строка. Ошибка')
            else:
                lines = self._read_catalog()
                par = par.lower()
                for i in lines[0]:
                    if par == i.lower():
                        print('Введённый параметр уже существует.')
                        break
                return par.title()

    def add_par(self):
        new_par = self.check_new_par()
        lines = self._read_catalog()
        lines[0].append(new_par)
        for i in lines[1:]:
            i.append('')
        self._write_catalog(lines)
        print('Параметр был добавлен')

    def del_par(self):
        lines = self._read_catalog()
        par = input('Введите параметр, который вы хотите удалить\n')
        if par.title() not in lines[0]:
            print('Введен несуществующий параметр')
        else:
            num = lines[0].index(par)
            for i in lines:
                del i[num]
            self._write_catalog(lines)
            print('Параметр был удален')


if __name__ == "__main__":
    auto_catalog = AutoCatalog()

    while True:
        print('ВЫБЕРИТЕ НУЖНУЮ ОПЦИЮ:')
        print('Введите "Показать" чтобы увидеть урезанный список и найти определенную строку')
        print('Введите "Показать все" чтобы увидеть все машины и их характеристики')
        print('Введите "Добавить" чтобы добавить машину')
        print('Введите "Искать" чтобы найти машину по фирме, модели или лицензии')
        print('Введите "Удалить" чтобы удалить машину')
        print('Введите "Изменить" чтобы изменить определенный параметр у машины')
        print('Введите "Стоп" чтобы остановить работу программы')
        print('Введите "Добавить параметр", чтобы появился новый параметр для каждой машины')
        print('Введите "Удалить параметр", чтобы удалить введенный параметр для каждой машины')

        command = input()

        if command.lower() == 'показать':
            auto_catalog.show_catalog()

        elif command.lower() == 'показать все':
            auto_catalog.show_all()

        elif command.lower() == 'добавить':
            auto_catalog.add_car()

        elif command.lower() == 'искать':
            auto_catalog.search_car()
        elif command.lower() == 'удалить':
            auto_catalog.delete_car()

        elif command.lower() == 'изменить':
            auto_catalog.update_car()

        elif command.lower() == 'стоп':
            break
        elif command.lower() == "добавить параметр":
            auto_catalog.add_par()

        elif command.lower() == "удалить параметр":
            auto_catalog.del_par()

        else:
            print('Неизвестная команда! Попробуйте заново\n')
