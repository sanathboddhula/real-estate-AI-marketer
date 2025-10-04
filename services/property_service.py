class PropertyService:
    @staticmethod
    def detect_property_type(price, bedrooms):
        """Detect property type for smart image search"""
        try:
            price_num = float(price.replace(',', '').replace('$', ''))
            bed_num = int(bedrooms)
            
            if price_num > 2000000:
                return "luxury"
            elif bed_num <= 2:
                return "modern"
            else:
                return "family"
        except:
            return "house"