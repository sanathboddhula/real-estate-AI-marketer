class MortgageService:
    @staticmethod
    def calculate_mortgage(price, down_payment_percent=20, interest_rate=6.5, loan_term_years=30):
        """Calculate monthly mortgage payment and related info"""
        try:
            price_num = float(str(price).replace(',', '').replace('$', ''))
            down_payment = price_num * (down_payment_percent / 100)
            loan_amount = price_num - down_payment
            
            # Monthly payment calculation
            monthly_rate = interest_rate / 100 / 12
            num_payments = loan_term_years * 12
            
            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
            else:
                monthly_payment = loan_amount / num_payments
            
            return {
                'monthly_payment': round(monthly_payment),
                'down_payment': round(down_payment),
                'loan_amount': round(loan_amount),
                'interest_rate': f"{interest_rate}%",
                'total_interest': round((monthly_payment * num_payments) - loan_amount)
            }
        except:
            return {
                'monthly_payment': 0,
                'down_payment': 0,
                'loan_amount': 0,
                'interest_rate': "6.5%",
                'total_interest': 0
            }