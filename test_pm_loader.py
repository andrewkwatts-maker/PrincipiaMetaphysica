import json

# Load theory_output.json
with open('theory_output.json', encoding='utf-8') as f:
    data = json.load(f)

# Check structure
print("=== TOP LEVEL KEYS ===")
print(list(data.keys()))

print("\n=== PARAMETERS KEYS ===")
if 'parameters' in data:
    print(list(data['parameters'].keys()))

    print("\n=== TOPOLOGY KEYS ===")
    if 'topology' in data['parameters']:
        topo = data['parameters']['topology']
        print(list(topo.keys()))
        print(f"\nB2 = {topo.get('B2')}")
        print(f"B3 = {topo.get('B3')}")
        print(f"CHI_EFF = {topo.get('CHI_EFF')}")
        print(f"n_gen = {topo.get('n_gen')}")

        # Test case-insensitive lookup (what pm-constants-loader should do)
        print("\n=== CASE INSENSITIVE TEST ===")
        for key in topo.keys():
            print(f"{key} -> {key.lower()}")
    else:
        print("NO TOPOLOGY IN PARAMETERS")
else:
    print("NO PARAMETERS KEY")
