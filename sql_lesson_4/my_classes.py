import contextlib
import psycopg2


class MyBase:
    def __init__(self, dbname, user, password, host, port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query: str, *args, one: bool = True) -> None:
        """выполнение запроса с базой"""
        with contextlib.suppress(Exception):
            self.cur.execute(query, *args)
            self.conn.commit()
            return self.cur.fetchone() if one else self.cur.fetchall()

    def add_new_client(self, f_name: str = None, l_name: str = None,
                       email: str = None, phone: int = None) -> str:
        """
        Функция, позволяющая добавить нового клиента.
        Вносим данные о клиенте имя, фамилия и почта обязательны,
        почта и телефон должны быть уникальными
        """
        if all((f_name, l_name, email)):
            if phone and self.execute_query("""SELECT *
                                                 FROM phones
                                                WHERE phone = %s;""", (phone,)):
                return f'{phone} не уникален, создание клиента отменено'
            if self.execute_query("""SELECT *
                                       FROM clients
                                      WHERE email = %s;""", (email,)):
                return f'{email} не уникален'
            client_id = (
                self.execute_query("""INSERT INTO clients(f_name, l_name, email)
                                      VALUES (%s, %s, %s)
                                   RETURNING client_id;""", (f_name, l_name, email)))
            if phone:
                self.execute_query("""INSERT INTO phones(phone, client_id)
                                      VALUES (%s, %s);""", (phone, client_id))
            return f'Добавлен {f_name} {l_name}'
        return 'Вы не ввели обязательное поле'

    def add_phone(self, client_id: int, number: int) -> str:
        """
        Функция, позволяющая добавить телефон для существующего клиента.
        """
        if self.execute_query("""SELECT *
                                   FROM phones
                                  WHERE phone = %s;""", (number,)):
            return f'{number} не уникален'
        if client := self.execute_query("""SELECT f_name, l_name
                                             FROM clients
                                            WHERE client_id = %s;""", (client_id,)):
            f, l = client
            self.execute_query("""INSERT INTO phones(phone, client_id)
                                  VALUES (%s, %s);""", (number, client_id))
            return f'Для {f} {l}, {client_id=} был добавлен номер телефона {number}'
        return f'Клиента с {client_id=} не существует'

    def change_client(self, client_id: int, first_name: str=None,
                      last_name: str=None, email: str=None) -> str:
        """Функция, позволяющая изменить данные о клиенте."""
        if any((first_name, last_name, email)):
            if first_name:
                self.execute_query("""UPDATE clients
                                         SET f_name = %s
                                       WHERE client_id = %s;""",
                                       (first_name, client_id,))
            if last_name:
                self.execute_query("""UPDATE clients
                                         SET l_name = %s
                                       WHERE client_id = %s;""",
                                       (last_name, client_id,))
            if email:
                self.execute_query("""UPDATE clients
                                         SET email = %s
                                       WHERE client_id = %s;""",
                                       (email, client_id,))
            res = self.execute_query("""SELECT f_name, l_name, email
                                          FROM clients
                                         WHERE client_id = %s;""", (client_id,))
            return f'{res} обновлен'
        return 'Вы не задали параметры которые необходимо обновить'

    def delete_phone(self, client_id: int, phone: int) -> str:
        """Функция, позволяющая удалить телефон для существующего клиента."""
        if self.execute_query("""DELETE FROM phones
                                  WHERE client_id = %s
                                    AND phone = %s
                              RETURNING *;""", (client_id, phone,)):
            return f'номер {phone} удален'
        return f'номер {phone} не найден у {client_id=}'

    def delete_client(self, client_id: int) -> str:
        """
        Функция, позволяющая удалить существующего клиента.
        """
        print('Предупреждение! Вместе с удалением '
              'клиента вы потеряете и контактные данные')
        answer = input('Уверены? Y/N... ')
        if answer.casefold() == 'y':
            if self.execute_query("""DELETE FROM clients
                                      WHERE client_id = %s
                                  RETURNING *;""", (client_id,)):
                return (f'клиент с {client_id=} удалён, так же были удалены'
                        f' связанные с ним данные')
            return f'клиент с {client_id=} не найден'
        return 'Вы не подтвердили удаление контакта'

    def find_client(self, first_name: str='%', last_name: str='%', email: str='%',
                    phone: int='%') -> list:
        """
        Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
        """
        phone = str(phone)
        return self.execute_query(
            """SELECT client_id, f_name, l_name, email, phone
                 FROM clients
                 JOIN phones USING(client_id)
                WHERE f_name LIKE %s
                  AND l_name LIKE %s
                  AND email LIKE %s
                  AND CAST(phone AS TEXT) LIKE %s;""",
                  (first_name, last_name, email, phone,), one=False)

    def __str__(self) -> str:
        return '\n'.join('  '.join(str(elem) for elem in x) for x in
            self.execute_query(query="""SELECT *
                                          FROM clients
                                          LEFT JOIN phones USING(client_id)""",
                                          one=False))

    def close_connection(self) -> None:
        """закрытие сессии"""
        self.cur.close()
        self.conn.close()
