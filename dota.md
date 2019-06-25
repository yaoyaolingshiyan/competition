# dota_paper_summary
## data statistic
* spatial resolution information : fine grained classification/filter mislabels
* img_quantity:2806
* ins_quantity:188282
* ins_category:15
* img_size:range from about 800*800 to about 4000*4000
* labeled by an arbitrary (8 d.o.f.) quadrilateral

![](dota_angles_and_size.PNG)
![](cate.PNG)

## data annotation
### arbitrary quadrilateral bounding box
### emphasize the importance of the first point(the head of the object)
* [left_head] helicopter, large vehicle, small vehicle, harbor, baseball diamond, ship, plane
* [top_left] soccer-ball field, swimming pool, bridge, ground track field, basketball court, tennis court
* [without_write] roundabout, storage tank
##
## distinguish from the conventional object detection
* The scale variations of object instances in aerial images are huge. This is not only because of the
spatial resolutions of sensors, but also due to the size variations inside the same object category.

* Many small object instances are crowded in aerial images, for example, the ships in a harbor
and the vehicles in a parking lot, as illustrated in Fig. 1. Moreover, the frequencies of instances
in aerial images are unbalanced, for example, some small-size (e.g. 1k × 1k) images contain
1900 instances, while some large-size images (e.g. 4k × 4k) may contain only a handfull of small
instances.

* Objects in aerial images often appear in arbitrary orientations. There are also some instances
with an extremely large aspect ratio, such as a bridge

## dataset compare
##
### instances size percentage
* the height of a horizontal bounding box as instance size
![](instance_size.PNG)
### aspect ratio of instances
![](AR_percentage.PNG)
### aerial objects dataset

![](aerial_dataset.PNG)

#### ideal conditions
* [39] UCAS-AOD
* [2]  NWPU VHR-10(10 categories)
#### only focus on vehicles
* [9] TAS
* [20] COWC
* [24] VEDAI
* [15] 3K Munich Vehicle
#### vehicles and planes
* [39] UCAS-AOD
#### only ships(fine-grained category)
* [17] HRSC2016

##
#### general objects datasets
![](general_dataset.PNG)


## compare with competition dataset
* category: 15/18 (airpoart, container-crane, helipad)
* quantity: 2806(1/2, 1/6, 1/3), 3206(1830, 593, 783)
* instances: 188282/349675(268627, 349675)
##
# Evalution
## crop image
* crop_size:1024*1024
* stride:512
* 目标在裁剪时被分开，如果 Ui<0.7, label = difficult

## testing phase
* first we send the cropped image patches to obtain temporary results and then
we combine the results together to restore the detecting results on the original image

![](result1.PNG)
1[](result2.PNG)
![](result3.PNG)


    


