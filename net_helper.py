#import os
import psutil

class NetworkInterfaceManager:
    def __init__(self):
        self._system_interfaces = self._get_system_interfaces()
        self._docker_interfaces = self._get_docker_interfaces()

    def _get_system_interfaces(self):
        """Private method to get system network interfaces (excluding Docker)."""
        interfaces = psutil.net_if_addrs().keys()
        return [iface for iface in interfaces if not iface.startswith("docker") and not iface.startswith("br-")]

    def _get_docker_interfaces(self):
        """Private method to get Docker-specific network interfaces."""
        interfaces = psutil.net_if_addrs().keys()
        return [iface for iface in interfaces if iface.startswith("docker") or iface.startswith("br-")]

    def get_all_interfaces(self):
        """Public method to return all interfaces (system + Docker)."""
        return self._system_interfaces + self._docker_interfaces

    def choose_interface_cli(self):
        """Public method for CLI interaction to choose a network interface."""
        interfaces = self.get_all_interfaces()

        print("Available network interfaces:")
        for idx, iface in enumerate(interfaces):
            print(f"{idx + 1}. {iface}")

        while True:
            try:
                choice = int(input("Select an interface by number: "))
                if 1 <= choice <= len(interfaces):
                    selected = interfaces[choice - 1]
                    print(f"Selected interface: {selected}")
                    return selected
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

# Example usage:
if __name__ == "__main__":
    manager = NetworkInterfaceManager()
    selected_interface = manager.choose_interface_cli()
