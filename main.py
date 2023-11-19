from selenium import webdriver
import time
import csv
import warnings

url = "<url_with_query_strings>"

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("user-data-dir=C:\\Users\\jan_m\\AppData\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 1')
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get(url), time.sleep(1.5)
driver.maximize_window()

print("Seite erfolgreich geladen. \nStart der extraktion...")
driver.find_element_by_xpath("/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-suche/ba-wbsuche-lib-suche/div/div/div[2]/ba-wbsuche-lib-suchergebnis/section/ba-wbsuche-lib-suchergebnis-header/div/div[2]/ba-bub-ansicht-switch/div/fieldset/div/div[2]").click()
time.sleep(0.2)

num_ergebnisse = int((driver.find_element_by_xpath('//*[@id="ergebniszaehler_text"]/span').get_attribute("innerText").replace(".", "")))

driver.find_element_by_xpath("/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-suche/ba-wbsuche-lib-suche/div/div/div[2]/ba-wbsuche-lib-suchergebnis/section/ba-wbsuche-lib-listen-ansicht/table/tbody/tr[1]/td[1]/a").click()

with open('kursnet.csv', 'w', newline='\n' ,encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["id", "headline", "anbieter", "beginn", "ende", "dauer", "laufender_einstieg", "unterrichtszeiten", "unterrichtszeit", "bemerkungen", "berufsbegleitend", "lernform", "praxistaileAG", "abschlussart",
    "gesamtkosten", "kosten_bemerkung", "bildungsgutschein", "zertifizierer", "förderung", "zugang", "zielgruppe", "teilnehmerzahl", "inhalt"])


    for _ in range(num_ergebnisse):
        time.sleep(0.2)
        headline = driver.find_element_by_xpath("/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/ba-wbsuche-lib-detail-header/div[2]/section/div[2]/h1").get_attribute("innerText")

        # Block Dauer
        beginn, ende, dauer, laufender_einstieg, unterrichtszeiten = "", "" , "", "", ""
        try:
            length_dauer = len(driver.find_element_by_xpath('//*[@id="detail_dauer_termine"]').get_property("children")) // 2
            try:
                for i in range(1, length_dauer +1):
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-dauer-termine/dl/dt[{i}]").get_attribute("innerText") == "Beginn":
                        beginn = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-dauer-termine/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dt[{i}]').get_attribute("innerText") == "Ende":
                        ende = driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dt[{i}]').get_attribute("innerText") == "Dauer":
                        dauer = driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dt[{i}]').get_attribute("innerText") == "Laufender Einstieg":
                        laufender_einstieg = driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dt[{i}]').get_attribute("innerText") == "Unterrichtszeiten":
                        unterrichtszeiten = driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dt[{i}]').get_attribute("innerText") == "Bemerkungen":
                        bemerkungen = driver.find_element_by_xpath(f'//*[@id="detail_dauer_termine"]/dd[{i}]').get_attribute("innerText").strip().replace("\n","")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)   


        # Block Weiterbildungsinformationen
        bildungsart, unterrichtszeit, berufsbegleitend, lernform, praxistaileAG, abschlussart, schulart = "", "", "", "", "", "", ""
        try:
            length_weiterbildungsinfos = len(driver.find_element_by_xpath('//*[@id="detail_wbinfo_marg"]').get_property("children")) // 2
            try:
                for i in range(1, length_weiterbildungsinfos +1):
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Bildungsart":
                        bildungsart = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Unterrichtszeit":
                        unterrichtszeit = driver.find_element_by_xpath(
                            '//*[@id="_marg_wbinfo_uzeit"]/ba-bub-chip/div/div[2]'
                        ).get_attribute("innerText")

                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Berufsbegleitend":
                        berufsbegleitend = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Lernform":
                        lernform = driver.find_element_by_xpath(
                            '//*[@id="_marg_wbinfo_uform"]/ba-bub-chip/div/div[2]'
                        ).get_attribute("innerText")

                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Praxisanteile beim Arbeitgeber":
                        praxistaileAG = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Schulart":
                        schulart = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Schulart":
                        schulart = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Abschlussart":
                        abschlussart = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Schulart":
                        schulart = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[2]/ba-wbsuche-lib-detail-kachel[2]/section/ba-wbsuche-lib-weiterbildungsinformationen/dl/dd[{i}]").get_attribute("innerText")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        # Block Kosten/Gebühren/Förderung
        try:
            gesamtkosten, kosten_bemerkung, bildungsgutschein, zertifizierer, förderung = "", "", "", "", ""
            length_kosten = len(driver.find_element_by_xpath('//*[@id="detail_kosten_gebuehren"]').get_property("children")) // 2
            try:
                for i in range(1, length_kosten +1):
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/ba-wbsuche-lib-detail-kachel[3]/section/ba-wbsuche-lib-kosten-gebuehren/dl/dt[{i}]").get_attribute("innerText") == "Gesamtkosten":
                        gesamtkosten = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/ba-wbsuche-lib-detail-kachel[3]/section/ba-wbsuche-lib-kosten-gebuehren/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dt[{i}]').get_attribute("innerText") == "Kosten-Bemerkung":
                        kosten_bemerkung = driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dt[{i}]').get_attribute("innerText") == "Zulassung zur Förderung mit Bildungsgutschein":
                        bildungsgutschein = driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dt[{i}]').get_attribute("innerText") == "Zertifizierer":
                        zertifizierer = driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dt[{i}]').get_attribute("innerText") == "Förderung":
                        förderung = driver.find_element_by_xpath(f'//*[@id="detail_kosten_gebuehren"]/dd[{i}]').get_attribute("innerText")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        # Block Zugangsinformationen
        zugang, zielgruppe, teilnehmerzahl = "", "", ""
        try:
            length_zugang = len(driver.find_element_by_xpath('//*[@id="detail_zuganginfo"]').get_property("children")) // 2
            try:
                for i in range(1, length_zugang +1):
                    if driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/div[1]/ba-wbsuche-lib-detail-kachel/section/ba-wbsuche-lib-zugangsinformationen/dl/dt[{i}]").get_attribute("innerText") == "Zugang":
                        zugang = driver.find_element_by_xpath(f"/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/div/ba-wbsuche-lib-details/div/div[1]/div[1]/ba-wbsuche-lib-detail-kachel/section/ba-wbsuche-lib-zugangsinformationen/dl/dd[{i}]").get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_zuganginfo"]/dt[{i}]').get_attribute("innerText") == "Zielgruppe":
                        zielgruppe = driver.find_element_by_xpath(f'//*[@id="detail_zuganginfo"]/dd[{i}]').get_attribute("innerText")
                    if driver.find_element_by_xpath(f'//*[@id="detail_zuganginfo"]/dt[{i}]').get_attribute("innerText") == "Teilnehmerzahl":
                        teilnehmerzahl = " " + driver.find_element_by_xpath(f'//*[@id="detail_zuganginfo"]/dd[{i}]').get_attribute("innerText")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        # Block Weiterbildungsinhalte
        inhalt = driver.find_element_by_xpath('//*[@id="detail_inhalte"]').get_attribute("innerText")
        anbieter = driver.find_element_by_xpath('//*[@id="detail-header__name"]').get_attribute("innerText")
        id = driver.current_url[-9:]

        print("headline: " + headline)

        writer.writerow([id, headline, anbieter, beginn, ende, dauer, laufender_einstieg, unterrichtszeiten, unterrichtszeit, bemerkungen, berufsbegleitend, lernform, praxistaileAG, abschlussart,
         gesamtkosten, kosten_bemerkung, bildungsgutschein, zertifizierer, förderung, zugang, zielgruppe, teilnehmerzahl, inhalt])

        driver.find_element_by_xpath("/html/body/ba-wbsuche-app/ba-bub-main-layout/main/div/ba-wbsuche-app-detail/ba-wbsuche-lib-detail/ba-wbsuche-lib-detail-header/div[1]/ba-wbsuche-lib-detail-navigation/nav/div/div/button[3]").click()

