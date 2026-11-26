"""Your first Python program.

`print` writes text to the terminal. Python runs a file top to bottom, so
this single line is the whole program.

The `if __name__ == "__main__":` guard below is the Python convention for
"run this only when the file is executed directly, not when it is imported
by another file". Every file in this repo uses it, so you can both run a
file and reuse its functions elsewhere.
"""


def main() -> None:
    print("Hello, world!")
    name = input("请输入你的姓名：")
    age = input("请输入你的年龄：")
    welcome_message = f"欢迎你，{name}！你今年{age}岁，祝你学习 Python 愉快！"
    print(f"姓名：{name}")
    print(f"年龄：{age}")
    print(welcome_message)
    print("祝你学习 Python 愉快！")



if __name__ == "__main__":
    main()
