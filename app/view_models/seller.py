class SellerViewModel:
    pass


def get_seller_json(seller):
    return {
        'realname': seller.realname,
        'phone': seller.phone
    }