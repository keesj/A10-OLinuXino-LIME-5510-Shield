// Harwin connector M50-2122045

pad_depth=2.10;
pad_width=0.65;
pad_distance=5.70;
pitch=1.27;

module connector_pad(){
	square([pad_width,pad_depth]);
}

module connector_row(count){
	for (i = [0 : 1 : count -1]){
		translate([i * pitch ,0,0]) connector_pad();
	}
}

module connector_pads(cols,rows){
	for (f = [0 : 1 : cols -1]){
		translate([0,(pad_distance - pad_depth) * f,0])
		connector_row(rows);
	}
	translate([pad_width/2,pad_distance/2 - pitch/2 ,0]) circle(r=0.05, $fn=100);
   translate([pad_width/2,pad_distance/2 + pitch/2 ,0]) circle(r=0.05, $fn=100);
	translate([pad_width/2 + (rows -1) * pitch,pad_distance/2 - pitch/2 ,0]) circle(r=0.05, $fn=100);
translate([pad_width/2 + (rows -1) * pitch,pad_distance/2 + pitch/2 ,0]) circle(r=0.05, $fn=100);
 
}


connector_pads(2,20);