# ESTE CÓDIGO NÃO ESTÁ SENDO USADO PARA NADA NO MOMENTO
honeypot_list = []


def run(event_type, src_path):
    if event_type == "modified" and src_path in honeypot_list:
        print("Possible malicious activity detected")


if __name__ == "__main__":
    run()
