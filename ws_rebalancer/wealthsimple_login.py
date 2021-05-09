import click
import wealthsimple


class WealthSimpleLogin(wealthsimple.WSTrade):
    """Wraps the WealthSimple Trade API with a login interface. This class can
    is used to login to the client's WealthSimple account and interact with the
    WealthSimple Trade API.
    """

    def __init__(self, email, password, two_factor_auth=False):
        two_factor_callback = (
            self.two_factor_function if two_factor_auth else None)
        wealthsimple.WSTrade.__init__(self,
                                      email,
                                      password,
                                      two_factor_callback=two_factor_callback)

    def two_factor_function(self):
        """Retrieves the two-factor auth code from the client."""
        MFACode = ""
        while not MFACode:
            # Obtain user input and ensure it is not empty
            MFACode = click.prompt("Enter 2FA code")
        return MFACode
