# MSR 2021 Replication package

This is the replication package of the paper titled **Mining the ROS ecosystem for Green Architectural Tactics in Robotics and an Empirical Evaluation** and published at MSR 2021.

This study has been designed, developed, and reported by the following investigators:

- [Ivano Malavolta](https://www.ivanomalavolta.com) (Vrije Universiteit Amsterdam)
- [Katerina Chinnappan](http://katerinachinnppan.com/) (Vrije Universiteit Amsterdam)
- [Stan Swanborn](https://www.linkedin.com/in/stan-swanborn-0470b4a9) (Vrije Universiteit Amsterdam)
- [Grace A. Lewis](https://resources.sei.cmu.edu/library/author.cfm?authorID=4347) (Software Engineering Institute, Carnegie Mellon University)
- [Patricia Lago](https://www.cs.vu.nl/~patricia/Patricia_Lago/Home.html) (Vrije Universiteit Amsterdam)

For any information, interested researchers can contact us by sending an email to any of the investigators listed above.
The full dataset including raw data, mining scripts, and analysis scripts produced during the study are available below.

## How to cite this replication package
If the data or software contained in this replication package is helping your research, consider to cite it is as follows, thanks!

```

@inproceedings{MSR_2021_architectural_tactics,
  author = { Ivano Malavolta and Katerina Chinnappan and Stan Swanborn and Grace Lewis and Patricia Lago },
  title = { Mining the ROS ecosystem for Green Architectural Tactics in Robotics and an Empirical Evaluation },
  booktitle = { Proceedings of the 18th International Conference on Mining Software Repositories, {MSR} },
  year = { 2021 },
  pages = { To appear },
  month = { May },
  publisher = { ACM },
  address = { New York, NY },
  url = {http://www.ivanomalavolta.com/files/papers/MSR_2021_ros_architectural_tactics.pdf}
}

```

---
## Overview of the replication package

The replication package is structured according to the research questions of the study (RQ1 and RQ2) and it is composed of the following elements:

- [MSR_2021_ros_architectural_tactics.pdf](MSR_2021_ros_architectural_tactics.pdf): the scientific publication
- [Supplementary Material (RQ1).pdf](supplementary_material_RQ1.pdf): a 93-pages technical report providing the details about our mining activities and application of thematic analysis for identifying green architectural tactics for robotics software.
- [Supplementary Material (RQ2).pdf](supplementary_material_RQ2.pdf): a 75-pages technical report detailing the design, conduction, and results of the empirical assessment of the identified green tactics.
- [RQ1_data_software](RQ1_data_software): the raw data and mining source code related to all the activities we carried out for answering RQ1.
- [RQ2_data](RQ2_data): the raw data related to all the activities we carried out for answering RQ2.
- [RQ2_ros_implementation](RQ2_ros_implementation): the source code of the ROS-based system we implemented for performing the experiment in RQ2.