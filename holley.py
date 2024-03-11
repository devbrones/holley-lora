class HolleyMRMPacketParser:
    def __init__(self, hex_data):
        self.hex_data = hex_data
        self.header = None
        self.content = None
        self.parsed_data = {}

    def parse(self):
        self.parse_header()
        self.parse_content()
        return self.parsed_data

    def parse_header(self):
        header_byte = int(self.hex_data[:2], 16)
        self.header = {
            "mark": (header_byte >> 6) & 0x03,
            "identifier": (header_byte >> 1) & 0x1F,
            "status": header_byte & 0x01
        }
        self.parsed_data["Header"] = self.header

    def parse_content(self):
        if self.header["identifier"] == 7:
            self.parse_record_1()
        elif self.header["identifier"] == 8:
            self.parse_record_2()

    def parse_record_1(self):
        # TODO: Implement parsing logic for Record 1
        pass

    def parse_record_2(self):
        start_idx = 2
        fields_length = [10, 10, 10, 10, 10, 10, 6, 6, 6, 6, 8, 8]
        fields = ["1.8.0", "1.8.1", "1.8.2", "2.8.0", "2.8.1", "2.8.2", 
                  "Psum", "P(L1)", "P(L2)", "P(L3)", "Status Word", "Second index"]
        content = {}

        for i, field in enumerate(fields):
            field_data = self.hex_data[start_idx:start_idx + fields_length[i]]
            if field in ["1.8.0", "1.8.1", "1.8.2", "2.8.0", "2.8.1", "2.8.2"]:
                content[field] = self.interpret_hex_as_kWh(field_data)
            elif field in ["Psum", "P(L1)", "P(L2)", "P(L3)"]:
                content[field] = self.interpret_hex_as_W(field_data)
            elif field == "Second index":
                content[field] = int(field_data, 16)
            elif field == "Status Word":
                content[field] = self.interpret_status_word(field_data)
            start_idx += fields_length[i]

        self.parsed_data["Record 2"] = content

    @staticmethod
    def interpret_hex_as_kWh(hex_str):
        return int(hex_str, 16) * 0.1 / 1000  # Convert Wh to kWh

    @staticmethod
    def interpret_hex_as_W(hex_str):
        return int(hex_str, 16) * 0.1  # Convert to W

    @staticmethod
    def interpret_status_word(hex_str):
        # Convert hex to binary string (removing the '0b' prefix and padding with zeros)
        binary_str = bin(int(hex_str, 16))[2:].zfill(32)
        # Map each bit to its corresponding status
        status_descriptions = {
            "S08_Messwerk": "Anlauf" if binary_str[7] == '1' else "Off",
            "S09_Magnetische_Manipulation": "Ja" if binary_str[8] == '1' else "Nein",
            "S10_Klemmendeckel_Manipulation": "Ja" if binary_str[9] == '1' else "Nein",
            "S11_Energierichtung": "+A" if binary_str[10] == '1' else "-A",
            "S12_Energierichtung_L1": "+A" if binary_str[11] == '1' else "-A",
            "S13_Energierichtung_L2": "+A" if binary_str[12] == '1' else "-A",
            "S14_Energierichtung_L3": "+A" if binary_str[13] == '1' else "-A",
            "S15_Drehfeld_L1_L2_L3": "Ja" if binary_str[14] == '1' else "Nein",
            "S16_Ruecklaufsperre": "aktiv" if binary_str[15] == '1' else "inaktiv",
            "S17_Fehler_eichrelevant": "Ja" if binary_str[16] == '1' else "Nein",
            "S18_Spannung_L1": "vorhanden" if binary_str[17] == '1' else "nicht vorhanden",
            "S19_Spannung_L2": "vorhanden" if binary_str[18] == '1' else "nicht vorhanden",
            "S20_Spannung_L3": "vorhanden" if binary_str[19] == '1' else "nicht vorhanden",
        }
        return status_descriptions

    @staticmethod
    def interpret_hex_as_kWh(hex_str):
        return int(hex_str, 16) * 0.1 / 1000  # Convert Wh to kWh

    @staticmethod
    def interpret_hex_as_W(hex_str):
        return int(hex_str, 16) * 0.1  # Convert to W

# Example usage
hex_data = "1100000623CD00000623CD00000000000000000000000000000000000000000000610000000000610000000008010400483A68"
parser = HolleyMRMPacketParser(hex_data)
parsed_data = parser.parse()
print(format(parsed_data))

