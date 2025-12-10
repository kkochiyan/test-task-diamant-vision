# email_checker.py

import dns.resolver
import dns.exception
from email_validator import validate_email, EmailNotValidError
import sys

def get_domain(email: str) -> str:
    """Извлекает домен из email-адреса и проверяет формат."""
    try:
        validation_result = validate_email(email, check_deliverability=False)
        return validation_result.domain
    except EmailNotValidError as e:
        raise ValueError(f"Неверный формат email: {str(e)}")
    except TypeError:
        raise ValueError("Email должен быть строкой")

def domain_exists(domain: str) -> bool:
    """Проверяет наличие A-записи домена."""
    resolver = dns.resolver.Resolver()
    try:
        resolver.resolve(domain, 'A')
        return True
    except dns.resolver.NXDOMAIN:
        return False
    except dns.exception.DNSException:
        # Другие ошибки DNS, например, временные проблемы с резолвером.
        # В рамках задания считаем, что домен потенциально существует, но мы не можем его проверить.
        return True

def check_mx(domain: str) -> bool:
    """Проверяет наличие MX-записей для домена."""
    resolver = dns.resolver.Resolver()
    try:
        answer = resolver.resolve(domain, "MX")
        return len(answer) > 0
    except dns.exception.DNSException:
        return False

def get_status(email: str) -> str:
    """Определяет статус email-адреса."""
    try:
        domain = get_domain(email)
    except ValueError as e:
        return str(e)

    if not domain_exists(domain):
        return "домен отсутствует"

    if not check_mx(domain):
        return "MX-записи отсутствуют или некорректны"

    return "домен валиден"


if __name__ == '__main__':
    emails = sys.argv[1:]

    if not emails:
        print("Укажите email-адреса через пробел в качестве аргументов командной строки.")
        print("Пример: python email_checker.py user@example.com user2@gmail.com invalid-format")
    else:
        for email in emails:
            print(f"{email} -> {get_status(email)}")

