import matplotlib.pyplot as plt
import numpy as np

def get_polynomial_aproximation(number_of_lines_array,data,degree):
	fit_data = np.polyfit(number_of_lines_array,data,degree)
	xx = np.linspace(0,len(number_of_lines_array),1200)
	yy = np.polyval(fit_data,xx)

	return xx,yy

def find_fm_minimum(fit_feature_matcing_x,fit_feature_matcing_y):
	min_value = fit_feature_matcing_y[0]
	current_i = fit_feature_matcing_x[0]

	aproximation = 0.00007

	valid_points_x = []
	valid_points_y = []
	cut_points_x = []
	cut_points_y = []

	cutoff = 0

	for i in range(1,len(fit_feature_matcing_y)):
		if fit_feature_matcing_y[i] - fit_feature_matcing_y[i-1] <= aproximation:
			current_i = fit_feature_matcing_x[i]
			valid_points_x.append(fit_feature_matcing_x[i])
			valid_points_y.append(fit_feature_matcing_y[i])
		else:
			current_i = fit_feature_matcing_x[i]
			cutoff = i
			valid_points_x.append(fit_feature_matcing_x[i])
			valid_points_y.append(fit_feature_matcing_y[i])
			break
	for i in range(cutoff,len(fit_feature_matcing_y)):
		cut_points_x.append(fit_feature_matcing_x[i])
		cut_points_y.append(fit_feature_matcing_y[i])
	return current_i,valid_points_x,valid_points_y,cut_points_x,cut_points_y


data = open('log-taichi.txt','r')
line = data.readline()

number_of_lines_array = [0]
number_of_lines = 0

perceptual_data = []
gen_gan_data = []
feature_matcing_data = []
disc_gan_data = []

while line:
	line = data.readline()
	if not line:
		break
	data_per_line = line.split(';')
	perceptual = data_per_line[0]
	gen_gan = data_per_line[1]
	feature_matcing = data_per_line[2]
	disc_gan = data_per_line[3]

	perceptual_data.append(float(perceptual.split('-')[1]))
	gen_gan_data.append(float(gen_gan.split('-')[1]))
	feature_matcing_data.append(float(feature_matcing.split('-')[1]))
	disc_gan_data.append(float(disc_gan.split('-')[1].strip()))

	number_of_lines +=1
	number_of_lines_array.append(number_of_lines)
	#print(float(feature_matcing.split('-')[1]))

	#print(disc_gan_data,perceptual_data,gen_gan_data,feature_matcing_data,disc_gan_data)

number_of_lines_array.pop(-1)


degree = 10

fit_perceptual_x, fit_perceptual_y = get_polynomial_aproximation(number_of_lines_array,perceptual_data,degree)
fit_feature_matcing_x,fit_feature_matcing_y = get_polynomial_aproximation(number_of_lines_array,feature_matcing_data,degree)
fit_gen_gan_x,fit_gen_gan_y = get_polynomial_aproximation(number_of_lines_array,gen_gan_data,degree)
fit_disc_gan_x,fit_disc_gan_y = get_polynomial_aproximation(number_of_lines_array,disc_gan_data,degree)

plt.title("perceptual error")
#plt.plot(number_of_lines_array,perceptual_data,label="perceptual")
plt.plot(fit_perceptual_x,fit_perceptual_y,'-')
plt.xlabel("Epoches")
plt.ylabel("Error value")
#plt.plot(fit_perceptual_x,fit_perceptual_y,'-',label="error perceptual")

plt.savefig('perceptual.png')
plt.close()

#min_pos= find_fm_minimum(fit_feature_matcing_x,fit_feature_matcing_y)
plt.title("Feature Matcing error")
#plt.plot(number_of_lines_array,feature_matcing_data,label="feature_matcing")
#plt.plot(fit_feature_matcing_x,fit_feature_matcing_y,'-')
minimum,valid_points_x,valid_points_y,cut_points_x,cut_points_y = find_fm_minimum(fit_feature_matcing_x,fit_feature_matcing_y)

plt.plot(valid_points_x,valid_points_y,'-')
plt.plot(cut_points_x,cut_points_y,'--',color = 'r')

plt.axvline(x =minimum , color = 'g')
plt.xlabel("Epoches")
plt.ylabel("Error value")
#plt.axvline(x = min_pos, color='g', linestyle='-')

plt.savefig('feature_matcing.png')
plt.close()

plt.title("GAN error")
#plt.plot(number_of_lines_array,gen_gan_data,label="gen_gan")
plt.plot(fit_gen_gan_x,fit_gen_gan_y,'-')
#plt.savefig('gen_gan.png')
#plt.close()

#plt.plot(number_of_lines_array,disc_gan_data,label="disc_gan")
#plt.title("Discriminator  error")
plt.plot(fit_disc_gan_x,fit_disc_gan_y,'-')
plt.xlabel("Epoches")
plt.ylabel("Error value")
plt.legend(["Generator error","Discriminator error"],loc="center left")
plt.savefig('gan.png')
plt.close()