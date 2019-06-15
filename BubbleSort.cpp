// BubbleSort.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <random>

#define DATALEN 10

//打印数组信息
void printArray(int(&dataArray)[DATALEN])
{
	//C++11标准的for循环形式，只能用于迭代可迭代类型
	for (auto data : dataArray) {
		std::cout << data << " ";
	}

	std::cout << std::endl;
}
int main()
{
	//待排序数组
	int dataArray[DATALEN] = { 0 };

	//创建随机数生成器
	std::random_device rd;
	std::mt19937 gen(rd());
	//生成范围为1~100之间
	std::uniform_int_distribution<> dis(1, 100);

	//使用循环初始化数据
	for (int i = 0; i < DATALEN; ++i) {
		dataArray[i] = dis(gen);
	}

	//打印数据
	printArray(dataArray);

	//开始对数据进行排序
	//长度为n的数据，需要进行DATALEN-1次排序操作
	for (int i = 0; i < DATALEN - 1; ++i)
	{
		//每次排序，是将为排序区间中最大数找到，并移到排序区间
		//排序使用的方法是两两比较（a,b)，如果a>b就将a和b进行交换。
		//为了实现找到最大的数，需要使用一个循环来完成，循环的次数为DATALEN-(i + 1)
		for (int j = 0; j < DATALEN - i - 1; j++)
		{
			if (dataArray[j] > dataArray[j + 1])
			{
				int temp = dataArray[j + 1];
				dataArray[j + 1] = dataArray[j];
				dataArray[j] = temp;
			}
		}
	}

	//打印结果
	printArray(dataArray);
}