
class MonitorFinanziario:
    def __init__(self, api):
        self.api = api
        self.bilancio_iniziale = self.get_account_balance()

    def get_account_balance(self):
        """Ritorna il bilancio corrente del conto."""
        account = self.api.get_account()
        return float(account.cash)

    def percentuale_investita(self):
        """Calcola la percentuale del bilancio investito rispetto al bilancio iniziale."""
        bilancio_corrente = self.get_account_balance()
        delta = self.bilancio_iniziale - bilancio_corrente
        percentuale = (delta / self.bilancio_iniziale) * 100
        return percentuale

    def check_soglia_investimento(self):
        """Verifica se la percentuale investita supera il 2% del bilancio iniziale."""
        return self.percentuale_investita() > 2

