// useDeviceDetails.ts
import { useEffect, useState, useCallback } from "react";
import { Dimensions } from "react-native";
import * as Device from "expo-device";
import * as Battery from "expo-battery";
import * as Network from "expo-network";
import * as Location from "expo-location";

export interface DeviceDetails {
  brand: string;
  model: string;
  os: string;
  osVersion: string;
  deviceType: string;
  deviceId: string;
  memory: string;
  batteryLevel: string;
  batteryState: string;
  ipAddress: string;
  connectionType: string;
  screenResolution: string;
  region: string;
  location: string;
  city: string;
  country: string;
  defaultcurrency: string;
  countryCallingCode: string;
}

const fetchCountryDetails = async (countryName: string): Promise<string> => {
  try {
    const response = await fetch(
      `https://restcountries.com/v3.1/name/${countryName}`
    );
    const data = await response.json();
    const requiredData = {
      defaultcurrency: Object.keys(data[0]?.currencies)[0],
      callingCode:
        data[0]?.idd?.root +
        (data[0]?.idd?.suffixes && data[0]?.idd?.suffixes.length === 1
          ? data[0]?.idd?.suffixes[0]
          : ""),
    };
    return `${requiredData.defaultcurrency}, ${requiredData.callingCode}`;
  } catch (error) {
    console.error("Error fetching country calling code:", error);
    return "Unknown";
  }
};

export const useDeviceDetails = (): DeviceDetails => {
  const [deviceDetails, setDeviceDetails] = useState<DeviceDetails>({
    brand: "",
    model: "",
    os: "",
    osVersion: "",
    deviceType: "",
    deviceId: "",
    memory: "",
    batteryLevel: "",
    batteryState: "",
    ipAddress: "",
    connectionType: "",
    screenResolution: "",
    region: "",
    location: "",
    city: "",
    country: "",
    defaultcurrency: "",
    countryCallingCode: "",
  });

  const getDeviceDetails = useCallback(async () => {
    // Request Location Permission
    const { status } = await Location.requestForegroundPermissionsAsync();
    let location = "Permission Denied";
    let city = "Unknown";
    let country = "Unknown";
    let region = "Unknown";
    let defaultcurrency = "KES";
    let countryCallingCode = "+254";

    if (status === "granted") {
      const loc = await Location.getCurrentPositionAsync({});
      const reverseGeocode = await Location.reverseGeocodeAsync(loc.coords);
      location = `Lat: ${loc.coords.latitude}, Lng: ${loc.coords.longitude}`;
      city = reverseGeocode[0]?.city || "Unknown";
      region = reverseGeocode[0]?.region || "Unknown";
      country = reverseGeocode[0]?.country || "Unknown";
      const countryInfo = await fetchCountryDetails(country);
      const [defaultcurrency, countryCallingCode] = countryInfo.split(", ");
      console.log("Country Calling Code", countryCallingCode);
      console.log("Default Currency", defaultcurrency);
    }

    const brand = Device.brand || "Unknown";
    const model = Device.modelName || "Unknown";
    const os = Device.osName || "Unknown";
    const osVersion = Device.osVersion || "Unknown";
    const deviceType = Device.deviceType === 1 ? "Phone" : "Tablet";
    const deviceId = Device.osInternalBuildId || "Unknown";
    const memory = Device.totalMemory
      ? `${(Device.totalMemory / 1024 / 1024 / 1024).toFixed(2)} GB`
      : "Unknown";

    const batteryLevel = await Battery.getBatteryLevelAsync();
    const batteryState = await Battery.getBatteryStateAsync();
    const ipAddress = await Network.getIpAddressAsync();
    const networkState = await Network.getNetworkStateAsync();
    const connectionType = networkState?.type || "Unknown";

    const screenResolution = `${Dimensions.get("window").width}x${
      Dimensions.get("window").height
    }`;

    setDeviceDetails({
      brand,
      model,
      os,
      osVersion,
      deviceType,
      deviceId,
      memory,
      batteryLevel: batteryLevel
        ? (batteryLevel * 100).toFixed(0) + "%"
        : "Unknown",
      batteryState:
        batteryState === 1
          ? "Unplugged"
          : batteryState === 2
          ? "Charging"
          : "Full",
      ipAddress,
      connectionType,
      screenResolution,
      region,
      location,
      city,
      country,
      defaultcurrency,
      countryCallingCode,
    });
  }, []);

  useEffect(() => {
    getDeviceDetails();
  }, [getDeviceDetails]);

  return deviceDetails;
};
