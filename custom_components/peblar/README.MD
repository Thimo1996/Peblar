# Peblar Home Assistant Integration

The Peblar Home Assistant Integration provides seamless integration with Peblar devices, enabling monitoring and control directly from Home Assistant. This integration supports configuring connection details, authenticating with the Peblar API, and setting up sensors and number entities.

---

## Features

- **Connection Management:** Configure the IP address and access token for your Peblar device.
- **Sensors:** Monitor key metrics like charging current, total energy, session energy, and charge power.
- **Number Entities:** Control parameters such as maximum charging current.
- **Reauthentication Support:** Easily reauthenticate in case of API authentication errors.

---

## Installation

### Installation via HACS

1. Ensure that [HACS (Home Assistant Community Store)](https://hacs.xyz/) is installed in your Home Assistant setup.
2. Go to **HACS > Integrations**.
3. Click the three dots in the top-right corner and select **Custom Repositories**.
4. Add the URL of this repository and select `Integration` as the category.
5. Search for `Peblar` in HACS and click **Download**.

### Manual Installation

1. Download or clone the integration files.
2. Place the files in the `custom_components/peblar` directory within your Home Assistant configuration folder.

### Step 2: Restart Home Assistant

Restart Home Assistant to load the new integration.

### Step 3: Add the Integration

1. Navigate to **Settings > Devices & Services** in Home Assistant.
2. Click **Add Integration** and search for `Peblar`.
3. Follow the prompts to configure the integration.
---

## Configuration

When setting up the Peblar integration, you will need:

- **IP Address:** The IP address of your Peblar device.
- **Access Token:** The access token for authenticating with the Peblar API.


## Supported Entities

### Sensors

| Sensor                     | Unit               | Device Class | State Class      |
|----------------------------|--------------------|--------------|------------------|
| Charger Max Charging Current | mA                 | Current      | Measurement       |
| Charger Total Energy       | Wh                 | Energy       | Measurement       |
| Charger Session Energy     | Wh                 | Energy       | Measurement       |
| Charger Charge Power       | W                  | Power        | Measurement       |

### Number Entities

| Entity                     | Min Value | Max Value | Step | Description                  |
|----------------------------|-----------|-----------|------|------------------------------|
| Charger Max Charging Current | 0         | 20000     | 1    | Set the maximum charging current |

---

## Error Handling

### Common Errors

- **`cannot_connect`**: Unable to connect to the Peblar device. Check the IP address and ensure the device is online.
- **`invalid_auth`**: Authentication failed. Verify your access token.
- **`reauth_invalid`**: Reauthentication failed. Ensure the IP address and access token are correct.

### Reauthentication

If reauthentication is required:

1. Open the Peblar integration settings in Home Assistant.
2. Update the IP address and/or access token.
3. Save the changes to reauthenticate.

---

### Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For more information or support, please refer to the [Home Assistant documentation](https://www.home-assistant.io) or contact the integration maintainer.

