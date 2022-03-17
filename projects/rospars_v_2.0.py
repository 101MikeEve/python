import requests
import pandas as pd


def register_of_licens(i):
    html = requests.get('https://www.gosnadzor.ru/service/list/reestr_licences_99fz/?PAGEN_1={}'.format(i)).content
    df_list = pd.read_html(html)
    df_list20 = df_list[20]
    df_lst = df_list20['Номер лицензии']
    return df_lst


def company_card(alll):
    main_html = requests.get('https://www.gosnadzor.ru/service/list/reestr_licences_99fz/license.php?licNum={}'.format(alll)).content
    df_main_html = pd.read_html(main_html)[19]
    return pd.DataFrame(df_main_html).transpose()


def main(pages):
    for iterator_all in range(1, pages):

        loading_i = int((iterator_all - 1) / (pages - 2) * 50)
        print(f'\rLoading - [{"-" * loading_i}{" " * (50 - loading_i)}] - {loading_i * 2}%', end="")

        page_company = register_of_licens(iterator_all)
        if iterator_all == 1:
            ppars = company_card(page_company[0])
        for n in page_company:
            new = company_card(n)
            ppars = pd.concat([ppars, new[1:]], ignore_index=True)

    res_data = ppars[2:].set_axis(list(ppars[:1].transpose()[0]), axis=1)

    return res_data


if __name__ == '__main__':
    pages_ros = 100

    res_data = main(pages_ros)
    res_data.to_excel('out.xlsx', index=False)