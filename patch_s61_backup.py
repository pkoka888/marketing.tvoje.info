import base64
import os

def patch_script():
    input_file = 's61_backup_script.sh'
    output_file = 's61_backup_script_patched.sh'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return

    with open(input_file, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')

    patch1 = '    mysqldump --defaults-extra-file="$MY_CNF" okamih_shop 2>/dev/null | \\'
    replace1 = '''    mysqldump --defaults-extra-file="$MY_CNF" \\
      --ignore-table=okamih_shop.ps_layered_filter_block \\
      --ignore-table=okamih_shop.ps_connections \\
      --ignore-table=okamih_shop.ps_connections_page \\
      --ignore-table=okamih_shop.ps_connections_source \\
      --ignore-table=okamih_shop.ps_guest \\
      --ignore-table=okamih_shop.ps_statssearch \\
      --ignore-table=okamih_shop.ps_search_index \\
      --ignore-table=okamih_shop.ps_search_word \\
      okamih_shop 2>/dev/null | \\'''

    patch2 = '    mysqldump --defaults-extra-file="$MY_CNF" okamih_shop_sk 2>/dev/null | \\'
    replace2 = '''    mysqldump --defaults-extra-file="$MY_CNF" \\
      --ignore-table=okamih_shop_sk.ps_layered_filter_block \\
      --ignore-table=okamih_shop_sk.ps_connections \\
      --ignore-table=okamih_shop_sk.ps_connections_page \\
      --ignore-table=okamih_shop_sk.ps_connections_source \\
      --ignore-table=okamih_shop_sk.ps_guest \\
      --ignore-table=okamih_shop_sk.ps_statssearch \\
      --ignore-table=okamih_shop_sk.ps_search_index \\
      --ignore-table=okamih_shop_sk.ps_search_word \\
      okamih_shop_sk 2>/dev/null | \\'''

    if patch1 not in content:
        print("Warning: patch1 not found exactly in content")
    if patch2 not in content:
        print("Warning: patch2 not found exactly in content")

    content = content.replace(patch1, replace1)
    content = content.replace(patch2, replace2)

    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    patch_script()
