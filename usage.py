from figroot.core import Config


def main():
    cfg = Config("usage")
    print(f"{cfg['hello.bye.foo']=}")

    # Dot-notation
    print(f"{cfg=}")
    print(f"{cfg.hello=}")
    print(f"{cfg.hello.bye=}")
    print(f"{cfg.hello.bye.foo=}")


if __name__ == "__main__":
    main()
