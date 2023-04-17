from modules.account.forms import EmailForm, EmailOrUsernameForm


class RestorePasswordForm(EmailForm):
    pass


class RestorePasswordViaEmailOrUsernameForm(EmailOrUsernameForm):
    pass


class RemindUsernameForm(EmailForm):
    pass
