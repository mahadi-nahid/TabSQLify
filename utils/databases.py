def create_and_write_table(data, columns, conn):
    try:
        cur = conn.cursor()
        # Drop Table if Exists
        sql_drop = "DROP Table IF EXISTS T"
        cur.execute(sql_drop)

        # Create a SQL statement to create a table with the column names
        sql_create = "CREATE TABLE T ("
        for col in columns:
            sql_create += col + " TEXT, "
        sql_create = sql_create[:-2] + ")"

        # Execute the SQL statement
        cur.execute(sql_create)

        sql_insert = f"INSERT INTO T VALUES ({', '.join(['?' for _ in columns])})"
        # Execute the SQL statement for each row of data
        for row in data[1:]:
            cur.execute(sql_insert, row)
        return True
    except:
        return False

def run_query(sql, conn):
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    headers = [col[0] for col in cur.description]
    return headers, result

# ['nu-0', 'nu-14', 'nu-30', 'nu-117', 'nu-146', 'nu-165', 'nu-177', 'nu-179', 'nu-187', 'nu-209', 'nu-219',
# 'nu-228', 'nu-244', 'nu-245', 'nu-263', 'nu-271', 'nu-282', 'nu-286', 'nu-292', 'nu-296', 'nu-348', 'nu-364',
# 'nu-365', 'nu-395', 'nu-438', 'nu-442', 'nu-454', 'nu-461', 'nu-519', 'nu-532', 'nu-539', 'nu-548', 'nu-562',
# 'nu-570', 'nu-587', 'nu-593', 'nu-607', 'nu-635', 'nu-650', 'nu-659', 'nu-682', 'nu-709', 'nu-743', 'nu-775',
# 'nu-819', 'nu-822', 'nu-823', 'nu-825', 'nu-832', 'nu-851', 'nu-854', 'nu-898', 'nu-904', 'nu-919', 'nu-969',
# 'nu-973', 'nu-978', 'nu-999', 'nu-1004', 'nu-1027', 'nu-1052', 'nu-1068', 'nu-1072', 'nu-1084', 'nu-1120',
# 'nu-1125', 'nu-1127', 'nu-1143', 'nu-1157', 'nu-1185', 'nu-1205', 'nu-1213', 'nu-1229', 'nu-1259', 'nu-1262',
# 'nu-1275', 'nu-1308', 'nu-1322', 'nu-1349', 'nu-1372', 'nu-1382', 'nu-1387', 'nu-1406', 'nu-1414', 'nu-1448',
# 'nu-1494', 'nu-1498', 'nu-1514', 'nu-1516', 'nu-1523', 'nu-1557', 'nu-1561', 'nu-1577', 'nu-1586', 'nu-1644',
# 'nu-1652', 'nu-1671', 'nu-1682', 'nu-1707', 'nu-1746', 'nu-1754', 'nu-1780', 'nu-1783', 'nu-1794', 'nu-1815',
# 'nu-1818', 'nu-1824', 'nu-1848', 'nu-1849', 'nu-1854', 'nu-1859', 'nu-1899', 'nu-1902', 'nu-1910', 'nu-1936',
# 'nu-1941', 'nu-1963', 'nu-1992', 'nu-1998', 'nu-1999', 'nu-2037', 'nu-2100', 'nu-2110', 'nu-2118', 'nu-2136',
# 'nu-2202', 'nu-2219', 'nu-2246', 'nu-2247', 'nu-2341', 'nu-2359', 'nu-2360', 'nu-2400', 'nu-2403', 'nu-2406',
# 'nu-2443', 'nu-2444', 'nu-2467', 'nu-2483', 'nu-2523', 'nu-2527', 'nu-2537', 'nu-2540', 'nu-2559', 'nu-2564',
# 'nu-2653', 'nu-2659', 'nu-2671', 'nu-2679', 'nu-2709', 'nu-2711', 'nu-2717', 'nu-2729', 'nu-2746', 'nu-2765',
# 'nu-2777', 'nu-2789', 'nu-2793', 'nu-2816', 'nu-2837', 'nu-2879', 'nu-2900', 'nu-2921', 'nu-2928', 'nu-2949',
# 'nu-2976', 'nu-2986', 'nu-3015', 'nu-3030', 'nu-3036', 'nu-3043', 'nu-3053', 'nu-3104', 'nu-3110', 'nu-3130',
# 'nu-3135', 'nu-3158', 'nu-3168', 'nu-3178', 'nu-3195', 'nu-3205', 'nu-3213', 'nu-3217', 'nu-3233', 'nu-3245',
# 'nu-3253', 'nu-3267', 'nu-3268', 'nu-3290', 'nu-3312', 'nu-3318', 'nu-3337', 'nu-3349', 'nu-3353', 'nu-3388',
# 'nu-3389', 'nu-3401', 'nu-3417', 'nu-3419', 'nu-3456', 'nu-3471', 'nu-3477', 'nu-3528', 'nu-3532', 'nu-3535',
# 'nu-3536', 'nu-3545', 'nu-3552', 'nu-3560', 'nu-3573', 'nu-3632', 'nu-3660', 'nu-3709', 'nu-3755', 'nu-3761',
# 'nu-3763', 'nu-3781', 'nu-3876', 'nu-3893', 'nu-3907', 'nu-3914', 'nu-3933', 'nu-3940', 'nu-3971', 'nu-3984',
# 'nu-3990', 'nu-4013', 'nu-4022', 'nu-4027', 'nu-4044', 'nu-4054', 'nu-4063', 'nu-4082', 'nu-4101', 'nu-4133',
# 'nu-4139', 'nu-4151', 'nu-4185', 'nu-4229', 'nu-4233', 'nu-4242', 'nu-4253', 'nu-4321', 'nu-4335']
