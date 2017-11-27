name = ecc
config_file = example_config_scn3me_subm.py

run:
		python ./tests/31_ecc_test.py -v -v -t scn3me_subm
 
run_ex:
		python ./tests/19_bank_test.py -v -t scn3me_subm 

run_bank2:
		python ./tests/20_sram_2bank_t.py -v -t scn3me_subm 

run_noglade:
		./openram_t.py -v -n -o $(name) -p ./design_dir/$(name) $(config_file)

run_glade:
		glade design_dir/$(name)/$(name).gds

run_real:
		./openram.py -v -n -o $(name) -p ./design_dir/$(name) $(config_file)
		glade design_dir/$(name)/$(name).gds

magic:
		magic -T SCN3ME_SUBM.30

clean:
		rm *.pyc
		rm *.gds
