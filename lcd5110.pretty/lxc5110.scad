include <rounded_square.scad>

pcb_width=43.22;
pcb_depth=45.80;
pcb_height=1.07;

module_width=40.0;
module_depth=33.95;
module_height=3.75;
module_depth_displacement=6.70;//compared to the pcb

screen_width=36.42;
screen_depth=25.83;
screen_height=module_height - 0.1;
screen_corner_radius=5;
screen_depth_displacement=1.43;// Compared to the module
module_height_displacement=0.1; //mm 

module pbc() {
	color("blue")
	 translate([-pcb_width/2,0,0]) 
  		cube([pcb_width,pcb_depth,pcb_height]);
}

r=screen_corner_radius;

module mod(){
	difference() {
	color("grey")
 	translate([-module_width/2,module_depth_displacement,pcb_height]) 
  	cube([module_width,module_depth,module_height]);

	translate([-screen_width/2,module_depth_displacement + screen_depth_displacement,pcb_height ])
 	linear_extrude(height=screen_height * 2)
 	rounded_square(
			dim=[screen_width,screen_depth],
			corners=[r,r,r,r]);
	}
}
module screen(){
	color("Turquoise", 0.8)
	translate([-screen_width/2,module_depth_displacement + screen_depth_displacement,pcb_height ])
 	linear_extrude(height=screen_height)
 		rounded_square(
			dim=[screen_width,screen_depth],
			corners=[r,r,r,r]);
}

module pin(){
	color("yellow")
	cube([0.6,0.6,11]);
}
module pins(count){
	pitch =  2.54;
	for (i = [0: 1: count-1]){
		translate([i * pitch,0,0]) pin();
	}
}
$fn=100;
module holes(){ 
	translate([-pcb_width/2 + 1.7 + 2.6,1.7 + 0.5,0]) cylinder(r=1.7,h=4,center=false);
   translate([pcb_width/2 -1.7 - 2.6,1.7 + 0.5,0]) cylinder(r=1.7,h=4,center=false);
	translate([-pcb_width/2 + 1.7 + 2.6,pcb_depth - 1.7 -1,0]) cylinder(r=1.7,h=4,center=false);
   translate([pcb_width/2 -1.7 - 2.6,pcb_depth - 1.7 -1,0]) cylinder(r=1.7,h=4,center=false);
}

//projection(cut = true)
difference(){
union() {
	pbc();
	mod();
	screen();
   
}
translate ([-pcb_width/2 + 10.83,3.11,0]) pins(8);
holes();
}