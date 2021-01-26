K_DB_NAME                       = 'coffee_housing'
K_USER_TABLE_NAME               = 'user_table'
K_RAWBEAN_TABLE_NAME            = 'rawbean_table'
K_SUPPLIER_TABLE_NAME            = 'supplier_table'
K_CUSTOMER_TABLE_NAME            = 'customer_table'
K_PURCHASE_TABLE_NAME            = 'purchase_order_table'

K_DEBUG_PRINT                   = True
K_DEBUG_DB                      = 'db'
K_DEBUG_RAWBEAN                 = 'rawbean'
K_DEBUG_AUTH                    = 'auth'
K_DEBUG_GENERIC                 = 'generic'
K_DEBUG_ERROR                   = 'error'
K_DEBUG_SUPPLIER                = 'supplier'
K_DEBUG_CUSTOMER                = 'customer'
K_DEBUG_PURCHASE                = 'purchase'



K_RET_SUCCESS                   = 0
K_RET_USER_ALREADY_REGISTERED   = 1
K_RET_USER_NOT_REGISTERED       = 2
K_RET_USER_LOGGED_IN            = 3

K_RET_INVALID_PARAM             = -1
K_RET_VAL_DB_NOT_CONNECTED      = -2
K_RET_VAL_DB_CONNECTION_FAILED  = -3
K_RET_USER_LOGIN_FAILED         = -5

dbgopt                          = {K_DEBUG_GENERIC : True, K_DEBUG_ERROR : True, K_DEBUG_DB : False, K_DEBUG_RAWBEAN : True, K_DEBUG_AUTH : True, K_DEBUG_SUPPLIER : True, K_DEBUG_CUSTOMER : True ,
                                    K_DEBUG_PURCHASE: True}

def dbgprint(msg = '', opt = K_DEBUG_GENERIC):
    if(opt in dbgopt and dbgopt[opt]):
        print(msg)

