import jellyfish
import numpy as np

def channel(sent_signal):
    s = np.mean(abs(sent_signal)**2)
    print(s)
    print(len(sent_signal))
    if s <= 1:
        s = 1
    noise_power = (10**(-2.65))*s
    shift = np.exp(-2j*np.pi*np.random.rand())
    sent_signal = sent_signal*shift
    noise_std = np.sqrt(noise_power/2)
    rcv_signal = sent_signal + noise_std*np.random.randn(len(sent_signal))+ 1j*noise_std*np.random.randn(len(sent_signal))
    return rcv_signal

def serialize_complex(complex_vector,file_name):
    complex_vector = complex_vector.reshape(-1)
    np.savetxt(file_name,np.concatenate([np.real(complex_vector),
    np.imag(complex_vector)]))

def deserialize_complex(file_name):
    tx_data = np.loadtxt(file_name)
    N_sample = tx_data.size
    N_sample = N_sample//2
    #tx_data = np.clip(tx_data, -1.5,1.5)
    tx_data = tx_data[0:N_sample] + 1j*tx_data[N_sample:(2*N_sample)]
    return tx_data

def read_file(path):
    with open(path, encoding="utf-8") as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    return content

def write_final(text):
    with open("final.txt", "w+", encoding="utf-8") as file:
        file.write(text)

def compute_score(init):
    ini = read_file(init)[0]
    fin = read_file('final.txt')[0]
    diff = jellyfish.damerau_levenshtein_distance(ini, fin)

    print("Result is : ", fin)
    print("Number of different characters : ", diff)

    return diff

def encode(qam, init):
    initial_str = read_file(init) 
    result = qam.encode(initial_str[0])
    serialize_complex(result, "input.txt")

def decode(qam):
    content = deserialize_complex(read_file("output.txt"))
    content = [complex(c) for c in content]

    comps = qam.decode(content)
    finalText = comps_to_string(comps)
    write_final(finalText)

def comps_to_string(_bytes):
    chars = []
    for byte in _bytes:
        u = int('0b' + byte, 2)
        chars.append(chr(u))
    return ''.join(chars)