# sentinel


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="/FE/public/logo.png" alt="Logo" width="250" height="250">

<h2 align="center">Sentinel</h2>
<h3 align="center">Project for the course of "Internet Of Things" @ University Of Catania</h3>

  <p align="center">
Solution for industrial maintenance in complex tunnels, monitoring the position, status, and well-being of operators with battery-powered devices, external IP network, and a comprehensive administrative service based on AI.
  </p>
</div>



<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone Repository
   ```sh
   git clone https://github.com/freschidizona/sentinel.git
   ```
2. Build Docker Services
   ```sh
   docker compose build
   ```
3. Run Docker Compose
   ```sh
   docker compose up
   ```
4. Change the SSID and Password variables in the [Gateway main file](https://github.com/freschidizona/sentinel/tree/main/Gateway/src/main.cpp)
5. Flash the ESP32 devices (Bracelet, Anchor, Gateway)
6. Connect to the anchor's Wi-Fi to trigger a Captive Portal
7. Set the appropriate Anchor Id (sequential number) via the Captive Portal page



<!-- USAGE EXAMPLES -->
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->

_You can check the [Documentation](https://github.com/freschidizona/sentinel/tree/main/Sentinel.pdf)_ to understand how Sentinel works.


<!-- SCREENSHOTS -->
## Screenshots
<br />
<div align="center">
  <img src="/Screenshots/login.jpeg" alt="Logo" style="width:auto; height:500px">
  <br>Login page<hr>
  <img src="/Screenshots/ui.jpeg" alt="Logo"  style="width:auto; height:500px">
  <br>Home page<hr>
  <img src="/Screenshots/captive.png" alt="Logo" style="width:auto; height:250px">
  <br>Captive Portal<hr>
</div>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License
Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/freschidizona/sentinel](https://github.com/freschidizona/sentinel)
