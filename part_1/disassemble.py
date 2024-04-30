import sys

binary_file = None
binary_data = None

w0_registers = {
   '000': 'al',
   '001': 'cl',
   '010': 'dl',
   '011': 'bl',
   '100': 'ah',
   '101': 'ch',
   '110': 'dh',
   '111': 'bh'
}

w1_registers = {
   '000': 'ax',
   '001': 'cx',
   '010': 'dx',
   '011': 'bx',
   '100': 'sp',
   '101': 'bp',
   '110': 'si',
   '111': 'di'
}

def main():
   if len(sys.argv) != 2:
      print("Usage python3 disassemble.py <binary_file>")
      sys.exit(1)

   binary_file = sys.argv[1]

   try:
      ## Open our file and read the binary data
      with open(binary_file, 'rb') as f:
         binary_data = f.read()

      # Loop over binary_data in 2 byte chunks (Will work as long as we're following 16 bit instrutions)
      for i in range(0, len(binary_data), 2):
         # Assign the bytes to seperate variables for parsing
         byte1 = bin(binary_data[i])[2:] # Take the first 8 bytes (byte 1)
         byte2 = bin(binary_data[i + 1])[2:] # Take the next 8 bytes (byte 2)

         #Extract Opcode, d & w from byte 1
         opcode = byte1[:6] #bits 1-6
         d = byte1[6] # bit 7
         w = byte1[7] # bit 8

         #Extract mod, reg, r/m from byte 2
         mod = byte2[:2] #bits 1-2
         reg = byte2[2:5] #bits 3-5
         r_m = byte2[5:] #bits 6-8

         operand = handle_opcode(opcode)

         if w == '0':
            destination = w0_registers[r_m]
            source = w0_registers[reg]
         else:
            destination = w1_registers[r_m]
            source = w1_registers[reg]

         print(operand + " " + destination + ", " + source)

   except FileNotFoundError:
    print(f"Error: File '{binary_file}' not found")
    sys.exit(1)
   
def handle_opcode(opcode):
   match opcode:
      case '100010':
         return 'mov'
      case '111111':
         return 'push'
      case '100011':
         return 'pop'
      case '000000':
         return 'add'
      case '001010':
         return 'sub'
      case '001110':
         return 'cmp'
      case _:
         pass
    
if __name__ == "__main__":
    main()
