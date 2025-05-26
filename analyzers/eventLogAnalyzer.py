# eventLogAnalyzer.py
import xml.etree.ElementTree as ET

def analiz_et(log_dosyasi):
    tree = ET.parse(log_dosyasi)
    root = tree.getroot()

    namespace = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    events = root.findall('ns:Event', namespace)
    
    for event in events:
        event_id = event.find('ns:System/ns:EventID', namespace)
        if event_id is not None and event_id.text == '5379':
            print(f"Olay ID: {event_id.text}")
            # Burada diğer alanları da çekip yazdırabilirsiniz.

if __name__ == "__main__":
    analiz_et('event_5379.xml')
