import random

# Configuration settings
VOLTAGE_NOMINAL = 230  # nominal voltage in volts
VOLTAGE_DEVIATION_THRESHOLDS = {"low": 5, "medium": 10, "high": 20}  # deviation %

FREQUENCY_NOMINAL = 50  # nominal frequency in Hz
FREQUENCY_THRESHOLDS = {"stable": 0.5, "unstable": 1.0}  # frequency deviation

LOAD_IMBALANCE_THRESHOLDS = {"balanced": 10, "unbalanced": 20}  # load % deviation

# Output severity levels
SEVERITY_LEVELS = ["Low", "Moderate", "High"]

# Action based on severity
MITIGATION_ACTIONS = {
    "Low": "Adjust Capacitor Banks",
    "Moderate": "Balance Loads Dynamically",
    "High": "Isolate Faulty Section"
}

# Simulator functions
def generate_test_data(num_samples=10):
    data = []
    for _ in range(num_samples):
        voltage = random.uniform(210, 250)  # simulate voltage fluctuations
        frequency = random.uniform(49, 51)  # simulate frequency changes
        load_imbalance = random.uniform(0, 30)  # simulate imbalance
        data.append((voltage, frequency, load_imbalance))
    return data

# Fuzzification functions
def fuzzify_voltage(voltage):
    deviation = abs(voltage - VOLTAGE_NOMINAL) / VOLTAGE_NOMINAL * 100
    if deviation <= VOLTAGE_DEVIATION_THRESHOLDS["low"]:
        return "Low"
    elif deviation <= VOLTAGE_DEVIATION_THRESHOLDS["medium"]:
        return "Medium"
    else:
        return "High"

def fuzzify_frequency(frequency):
    deviation = abs(frequency - FREQUENCY_NOMINAL)
    if deviation <= FREQUENCY_THRESHOLDS["stable"]:
        return "Stable"
    else:
        return "Unstable"

def fuzzify_load_imbalance(imbalance_percentage):
    if imbalance_percentage <= LOAD_IMBALANCE_THRESHOLDS["balanced"]:
        return "Balanced"
    else:
        return "Unbalanced"

# Rules engine
def infer_severity(voltage_state, frequency_state, load_state):
    if voltage_state == "High" and frequency_state == "Unstable" and load_state == "Unbalanced":
        return "High"
    elif (voltage_state == "Medium" or frequency_state == "Unstable") and load_state == "Unbalanced":
        return "Moderate"
    elif voltage_state == "Medium" or frequency_state == "Unstable":
        return "Moderate"
    else:
        return "Low"

# Defuzzification
def decide_mitigation_action(severity):
    return MITIGATION_ACTIONS.get(severity, "Monitor System")

# Utility functions
def print_case(voltage, frequency, load_imbalance, severity, action):
    print(f"Voltage: {voltage:.2f} V | Frequency: {frequency:.2f} Hz | Load Imbalance: {load_imbalance:.2f}%")
    print(f"→ Severity Detected: {severity}")
    print(f"→ Suggested Action: {action}")
    print("-" * 50)

# Main execution
def main():
    test_data = generate_test_data(10)

    for voltage, frequency, load_imbalance in test_data:
        voltage_state = fuzzify_voltage(voltage)
        frequency_state = fuzzify_frequency(frequency)
        load_state = fuzzify_load_imbalance(load_imbalance)

        severity = infer_severity(voltage_state, frequency_state, load_state)
        action = decide_mitigation_action(severity)

        print_case(voltage, frequency, load_imbalance, severity, action)

if __name__ == "__main__":
    main()