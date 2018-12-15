# coding:utf-8
from jinja2 import Environment, FileSystemLoader


class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return self.name + ',' + str(self.age)


def main():
    env = Environment(loader=FileSystemLoader('./'))
    tpl = env.get_template('page_template.txt')

    with open('page.txt', 'w+') as fout:
        render_content = tpl.render(person=Person('Tom', 20))
        fout.write(render_content)


if __name__ == '__main__':
    main()
